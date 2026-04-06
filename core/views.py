from django.http import HttpResponse
from django.contrib import messages
from finance.models import Transacao
#from .models import Transacao
from finance.forms import TransacaoForm
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from calendar import month_name
from django.contrib.auth import views as auth_views #para autenticação
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from finance.forms import CadastroForm
from finance.forms import EditarContaForm
from django.contrib.auth import update_session_auth_hash
import calendar
from django.db.models import Sum



def teste_context_processor(request):
    return render(request, "finance/teste_context.html")


MESES_PT = [
    '', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

#ajustar home para exibir transações
def home(request):
    
    hoje = date.today()
    return redirect('mes_atual', ano=hoje.year, mes=hoje.month)
    
    transacoes = Transacao.objects.all().order_by('-data') #ordena da data mais recente para a mais antiga
    
    total_entradas = sum(
        t.valor for t in transacoes 
        if t.categoria.lower() == 'receita'
        )
    
    total_despesas = sum(
        t.valor for t in transacoes 
        if t.categoria.lower() == 'despesa'
        )
    
    saldo = total_entradas - total_despesas
     #nova funcionalidade para editar transação
    if request.method == "POST" and "transacao_id" in request.POST:
        transacao_id = request.POST.get("transacao_id")
        transacao_obj = get_object_or_404(Transacao, id=transacao_id)
        form = TransacaoForm(request.POST, instance=transacao_obj)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {
        "transacoes": transacoes,
        "total_entradas": total_entradas,
        "total_despesas": total_despesas,
        "saldo": saldo,
        "form": TransacaoForm() #formulario vazio para o modal
    } #ajustar para exibir transações, entradas, despesas e saldo

    return render(request, "finance/mes_atual.html", context)  # renderiza o template mes_atual.html com o contexto  

#nova view para excluir transação
def excluir_transacao(request, transacao_id):
    transacao = get_object_or_404(Transacao, id=transacao_id)
    transacao.delete()
    messages.success(request, f"Transação '{transacao.descricao}' excluída com sucesso.")
    
    referer = request.META.get('HTTP_REFERER') # faz o redirecionamento para a página anterior
    if referer:
        return redirect(referer)    
    else:
        hoje = date.today()
    return redirect('mes_atual', ano=hoje.year, mes=hoje.month)


def sobre(request): #request é o objeto que contém todas as informações sobre a requisição HTTP feita pelo cliente
    return render(request, "finance/sobre.html") #o render substitui o HttpResponse, facilitando a renderização de templates

def listar_transacoes(request):
    return render(request, "finance/listar_transacoes.html")

def nova_transacao(request): # Função para lidar com a criação de uma nova transação
    if request.method == 'POST': # Verifica se o formulário foi enviado via POST
        form = TransacaoForm(request.POST)
        if form.is_valid():
            Transacao = form.save(commit=False)
            Transacao.user = request.user  # Atribui o usuário atual à transação
            Transacao.save()
            messages.success(request, 'Transação adicionada com sucesso!')
            return redirect('mes_atual') # Redireciona para a página inicial toda vez que uma nova transação é criada
    else:
        form = TransacaoForm()
        
    return render(request, 'finance/nova_transacao.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username'] # isso faz com que o sistema pegue o username e a senha do formulário de login
        #email = request.POST['email']
        password = request.POST['password'] 
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('mes_atual')
        else:
            
            messages.error(request, 'Credenciais inválidas. Por favor, tente novamente.')
            
    return render(request, 'finance/login.html')

def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('mes_atual')
        else:
            messages.error(request, 'Credenciais inválidas. Por favor, tente novamente.')
    else:
        form = CadastroForm()  # ← Aqui cria o form quando for apenas abrir a página

    return render(request, 'finance/cadastro.html', {'form': form})


def logout_view(request):
    
    logout(request)
    return redirect('login')



@login_required
def excluir_conta(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Sua conta foi excluída com sucesso.')
        return redirect('cadastro')
    return render(request, 'finance/excluir_conta.html')


# EDITAR CONTA
@login_required
def editar_conta(request):
    
    user = request.user # pega o usuário logado atualmente
    
    if request.method == "POST":
        form = EditarContaForm(user, request.POST)

        if form.is_valid():

            # Atualiza nome e email
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()

            # Atualiza senha, se informada
            if form.cleaned_data.get('new_password1'):
                form.save()
                update_session_auth_hash(request, user)

            messages.success(request, "Conta atualizada com sucesso!")
            return redirect("editar_conta")

    else:
        form = EditarContaForm(user)

    return render(request, "finance/editar_conta.html", {"form": form})

# LISTAR USUÁRIOS
@user_passes_test(lambda u: u.is_superuser) # faz com que apenas administradores possam acessar essa view
def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'finance/listar_usuarios.html', {'usuarios': usuarios})

@login_required
def mes_atual(request, ano=None, mes=None):
    from datetime import date
    from datetime import datetime
    
    hoje = date.today()
    agora = datetime.now()
    

    if not ano or not mes:
        ano = hoje.year
        mes = hoje.month
    
    # cálculo de mês anterior
    if mes == 1:
        mes_anterior = 12
        ano_anterior = ano - 1
    else:
        mes_anterior = mes - 1
        ano_anterior = ano
    # cálculo de próximo mês
    if mes == 12:
        mes_proximo = 1
        ano_proximo = ano + 1
    else:
        mes_proximo = mes + 1
        ano_proximo = ano
    
    mes_nome = MESES_PT[mes]
    mes_anterior_nome = MESES_PT[mes_anterior]
    mes_proximo_nome = MESES_PT[mes_proximo]


    # filtra transações, calcula totais etc.
    transacoes = Transacao.objects.filter(
        user = request.user,
        data__year=ano, 
        data__month=mes
        )
    
    total_entradas = sum(t.valor for t in transacoes if t.categoria == 'receita')
    total_saidas = sum(t.valor for t in transacoes if t.categoria == 'despesa')
    total_guardar = total_entradas - total_saidas
    
    
    if request.method == "POST" and "transacao_id" in request.POST:
        
        transacao_id = request.POST.get("transacao_id")
        transacao_obj = get_object_or_404(Transacao, id=transacao_id, user=request.user)
        form = TransacaoForm(request.POST, instance=transacao_obj)
        
        if form.is_valid():
            
            transacao = form.save(commit=False)
            transacao.user = request.user
            transacao.save()
            messages.success(request, "Transação atualizada com sucesso!")
            return redirect("mes_atual")  # redireciona pra o mês atual

    context = {
        'ano': ano,
        'mes': mes,
        'mes_nome': mes_nome,
        'ano_anterior': ano_anterior,
        'mes_anterior': mes_anterior,
        'mes_anterior_nome': mes_anterior_nome,
        'ano_proximo': ano_proximo,
        'mes_proximo': mes_proximo,
        'mes_proximo_nome': mes_proximo_nome,
        'transacoes': transacoes,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'total_guardar': total_guardar,
        'data_atual': agora,
    }
    return render(request, 'finance/mes_atual.html', context)

def mes_atual_padrao(request):
    hoje = date.today()

    
    return redirect('mes_atual', ano=hoje.year, mes=hoje.month)


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
        "mes_nome": calendar.month_name[mes],
        "ano_anterior": ano_anterior,
        "mes_anterior": mes_anterior,
        "mes_anterior_nome": calendar.month_name[mes_anterior],
        "ano_proximo": ano_proximo,
        "mes_proximo": mes_proximo,
        "mes_proximo_nome": calendar.month_name[mes_proximo],
        "total_entradas":entradas,
        "total_saidas": saidas,
        "total_guardar": guardar,
        
        "total_prev_entradas": Decimal(0),  # Substitua pelo valor previsto de entradas
        "total_prev_saidas": Decimal(0),  # Substitua pelo valor previsto de saídas
        "total_prev_guardar": Decimal(0),  # Substitua pelo valor previsto de guardar
       
    }
    return render(request, "finance/grafico_mes.html", context)




def editar_transacao(request, transacao_id):
    transacao = get_object_or_404(Transacao, id=transacao_id)

    if request.method == "POST":
        transacao.descricao = request.POST.get("descricao")
        transacao.valor = request.POST.get("valor")
        transacao.data = request.POST.get("data")
        transacao.categoria = request.POST.get("categoria")
        transacao.pago = bool(request.POST.get("pago"))
        transacao.save()
        return redirect('home')
