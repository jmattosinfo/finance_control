from django.http import HttpResponse
from django.contrib import messages
from finance.models import Transacao
#from .models import Transacao
from finance.forms import TransacaoForm
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from calendar import month_name

from django.shortcuts import redirect

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
            form.save()
            return redirect('mes_atual') # Redireciona para a página inicial toda vez que uma nova transação é criada
    else:
        form = TransacaoForm()
        
    return render(request, 'finance/nova_transacao.html', {'form': form})

from calendar import month_name

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
    transacoes = Transacao.objects.filter(data__year=ano, data__month=mes)
    total_entradas = sum(t.valor for t in transacoes if t.categoria == 'receita')
    total_saidas = sum(t.valor for t in transacoes if t.categoria == 'despesa')
    total_guardar = total_entradas - total_saidas
    
    
    if request.method == "POST" and "transacao_id" in request.POST:
        transacao_id = request.POST.get("transacao_id")
        transacao_obj = get_object_or_404(Transacao, id=transacao_id)
        form = TransacaoForm(request.POST, instance=transacao_obj)
        if form.is_valid():
            form.save()
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


def grafico_mes(request, ano, mes):
    # aqui você pode passar os mesmos dados do mes_atual para o gráfico
    context = {
        "ano": ano,
        "mes": mes,
        # se quiser, pode passar totais ou transações
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
