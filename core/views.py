from django.http import HttpResponse
from django.contrib import messages
from finance.models import Transacao
#from .models import Transacao
from finance.forms import TransacaoForm
from django.shortcuts import render, redirect, get_object_or_404

from django.shortcuts import redirect

#ajustar home para exibir transações
def home(request):
    transacao = Transacao.objects.all().order_by('-data') #ordena da data mais recente para a mais antiga
    
    total_entradas = sum(
        t.valor for t in transacao 
        if t.categoria.lower() == 'receita'
        )
    
    total_despesas = sum(
        t.valor for t in transacao 
        if t.categoria.lower() == 'despesa'
        )
    
    saldo = total_entradas - total_despesas
    
    return render(request, "finance/home.html", {
        "transacao": transacao,
        "total_entradas": total_entradas,
        "total_despesas": total_despesas,
        "saldo": saldo        
        }) #ajustar para exibir transações, entradas, despesas e saldo

#nova view para excluir transação
def excluir_transacao(request, transacao_id):
    transacao = get_object_or_404(Transacao, id=transacao_id)
    transacao.delete()
    messages.success(request, f"Transação '{transacao.descricao}' excluída com sucesso.") #mensagem de sucesso após excluir a transação
    return redirect('home') #redireciona para a página inicial após excluir a transação

def sobre(request): #request é o objeto que contém todas as informações sobre a requisição HTTP feita pelo cliente
    return render(request, "finance/sobre.html") #o render substitui o HttpResponse, facilitando a renderização de templates

def listar_transacoes(request):
    return render(request, "finance/listar_transacoes.html")


def nova_transacao(request): # Função para lidar com a criação de uma nova transação
    if request.method == 'POST': # Verifica se o formulário foi enviado via POST
        form = TransacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') # Redireciona para a página inicial toda vez que uma nova transação é criada
    else:
        form = TransacaoForm()
        
    return render(request, 'finance/nova_transacao.html', {'form': form})
