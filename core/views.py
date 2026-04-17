from django.http import HttpResponse
from django.contrib import messages
from finance.models import Transacao, Membro, Previsao # Importados os novos modelos
from finance.forms import TransacaoForm, CadastroForm, EditarContaForm
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, datetime
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods
from django.db.models import Sum
from decimal import Decimal

MESES_PT = [
    '', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

@login_required
def home(request):
    hoje = date.today()
    return redirect('mes_atual', ano=hoje.year, mes=hoje.month)

@login_required
def mes_atual(request, ano=None, mes=None):
    hoje = date.today()
    agora = datetime.now()

    if not ano or not mes:
        ano, mes = hoje.year, hoje.month

    # --- LÓGICA DE NAVEGAÇÃO ---
    if mes == 1:
        mes_anterior, ano_anterior = 12, ano - 1
        mes_proximo, ano_proximo = 2, ano
    elif mes == 12:
        mes_anterior, ano_anterior = 11, ano
        mes_proximo, ano_proximo = 1, ano + 1
    else:
        mes_anterior, ano_anterior = mes - 1, ano
        mes_proximo, ano_proximo = mes + 1, ano

    # --- SALDO MÊS ANTERIOR (Sua planilha: "Saldo Mês Anterior") ---
    transacoes_passadas = Transacao.objects.filter(
        user=request.user, 
        data__year=ano_anterior, 
        data__month=mes_anterior
    )
    entradas_passadas = transacoes_passadas.filter(categoria='receita').aggregate(Sum('valor'))['valor__sum'] or 0
    saidas_passadas = transacoes_passadas.filter(categoria='despesa').aggregate(Sum('valor'))['valor__sum'] or 0
    saldo_mes_anterior = entradas_passadas - saidas_passadas

    # --- FILTROS DO MÊS ATUAL ---
    transacoes = Transacao.objects.filter(
        user=request.user,
        data__year=ano, 
        data__month=mes
    ).order_by('data_vencimento', 'data')

    previsoes = Previsao.objects.filter(user=request.user, mes_referencia=mes, ano_referencia=ano)

    # --- TOTAIS ATUAIS ---
    total_entradas = transacoes.filter(categoria='receita').aggregate(Sum('valor'))['valor__sum'] or 0
    total_saidas = transacoes.filter(categoria='despesa').aggregate(Sum('valor'))['valor__sum'] or 0
    
    total_bruto = total_entradas + saldo_mes_anterior # Receitas + o que sobrou
    saldo_final = total_bruto - total_saidas

    # --- DADOS PARA O GRÁFICO (Previsto vs Realizado) ---
    total_prev_entradas = previsoes.filter(categoria='receita').aggregate(Sum('valor_previsto'))['valor_previsto__sum'] or 0
    total_prev_saidas = previsoes.filter(categoria='despesa').aggregate(Sum('valor_previsto'))['valor_previsto__sum'] or 0

    # Lógica de salvar via POST no Dashboard
    if request.method == "POST" and "transacao_id" in request.POST:
        transacao_id = request.POST.get("transacao_id")
        transacao_obj = get_object_or_404(Transacao, id=transacao_id, user=request.user)
        form = TransacaoForm(request.user, request.POST, instance=transacao_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Transação atualizada com sucesso!")
            return redirect("mes_atual", ano=ano, mes=mes)
        form = TransacaoForm(user=request.user)

    context = {
        
        'form':TransacaoForm(request.user),
        'ano': ano, 'mes': mes, 'mes_nome': MESES_PT[mes],
        'ano_anterior': ano_anterior, 'mes_anterior': mes_anterior, 'mes_anterior_nome': MESES_PT[mes_anterior],
        'ano_proximo': ano_proximo, 'mes_proximo': mes_proximo, 'mes_proximo_nome': MESES_PT[mes_proximo],
        'saldo_mes_anterior': saldo_mes_anterior,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'total_bruto': total_bruto,
        'total_guardar': saldo_final,
        'transacoes': transacoes,
        'previsoes': previsoes,
        'total_prev_entradas': total_prev_entradas,
        'total_prev_saidas': total_prev_saidas,
        'total_prev_guardar': total_prev_entradas - total_prev_saidas,
        'data_atual': agora,
    }
    return render(request, 'finance/mes_atual.html', context)

@login_required
def nova_transacao(request):
    if request.method == 'POST':
        form = TransacaoForm(request.user, request.POST) # Passando request.user para o form
        if form.is_valid():
            nova_transacao_obj = form.save(commit=False)
            nova_transacao_obj.user = request.user
            nova_transacao_obj.save()
            messages.success(request, 'Transação adicionada!')
            return redirect('home')
    else:
        form = TransacaoForm(request.user)
    return render(request, 'finance/nova_transacao.html', {'form': form})

@login_required
def excluir_transacao(request, transacao_id):
    transacao = get_object_or_404(Transacao, id=transacao_id, user=request.user)
    transacao.delete()
    messages.success(request, "Transação excluída.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

# --- VIEWS DE AUTENTICAÇÃO E PERFIL (MANTIDAS) ---
def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Credenciais inválidas.')
    return render(request, 'finance/login.html')

def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('home')
    else:
        form = CadastroForm()
    return render(request, 'finance/cadastro.html', {'form': form})

@login_required
def editar_conta(request):
    user = request.user
    if request.method == "POST":
        form = EditarContaForm(user, request.POST)
        if form.is_valid():
            user.username, user.email = form.cleaned_data['username'], form.cleaned_data['email']
            user.save()
            if form.cleaned_data.get('new_password1'):
                form.save()
                update_session_auth_hash(request, user)
            messages.success(request, "Conta atualizada!")
            return redirect("editar_conta")
    else:
        form = EditarContaForm(user)
    return render(request, "finance/editar_conta.html", {"form": form})

@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    return redirect('login')

def mes_atual_padrao(request):
    hoje = date.today()
    return redirect('mes_atual', ano=hoje.year, mes=hoje.month)

def sobre(request):
    return render(request, "finance/sobre.html")

def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'finance/listar_usuarios.html', {'usuarios': usuarios})

def listar_transacoes(request):
    return render(request, "finance/listar_transacoes.html")

def editar_transacao(request, transacao_id):
    return redirect('home')


def grafico_mes(request, ano, mes): # calcular mês anterior e próximo
            
    mes_anterior = mes - 1 if mes > 1 else 12
    ano_anterior = ano if mes > 1 else ano - 1

    mes_proximo = mes + 1 if mes < 12 else 1
    ano_proximo = ano if mes < 12 else ano + 1
    
    from decimal import Decimal
    
    transacoes = Transacao.objects.filter(data__year=ano, data__month=mes)    
    entradas = transacoes.filter(categoria__iexact="receita").aggregate(Sum("valor"))["valor__sum"] or 0
    saidas = transacoes.filter(categoria__iexact="despesa").aggregate(Sum("valor"))["valor__sum"] or 0
    guardar = entradas - saidas

    context = {
        "ano": ano,
        "mes": mes,
        "mes_nome": MESES_PT[mes],
        "ano_anterior": ano_anterior,
        "mes_anterior": mes_anterior,
        "mes_anterior_nome": MESES_PT[mes_anterior],
        "ano_proximo": ano_proximo,
        "mes_proximo": mes_proximo,
        "mes_proximo_nome": MESES_PT[mes_proximo],
        "total_entradas":entradas,
        "total_saidas": saidas,
        "total_guardar": guardar,
        
        "total_prev_entradas": Decimal(0),  # Substitua pelo valor previsto de entradas
        "total_prev_saidas": Decimal(0),  # Substitua pelo valor previsto de saídas
        "total_prev_guardar": Decimal(0),  # Substitua pelo valor previsto de guardar
       
    }
    return render(request, "finance/grafico_mes.html", context)

def teste_context_processor(request):
    return render(request, "finance/teste_context.html")

def excluir_conta(request):
    return render(request, 'finance/excluir_conta.html')
# Outras views (sobre, listar_usuarios, etc) permanecem as mesmas.