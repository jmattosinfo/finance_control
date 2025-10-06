# views.py são responsáveis por lidar com as requisições HTTP, processar dados e retornar respostas. 
# Por exemplo, renderizar templates HTML ou retornar dados em formato JSON. JSON são usados para APIs.
# Aqui você define funções ou classes que recebem uma requisição e retornam uma resposta.

from django.shortcuts import render
from django.http import HttpResponse
from .models import Transacao
from .forms import TransacaoForm
from django.shortcuts import render

def listar_transacoes(request):
    transacoes = Transacao.objects.all()  # Obtém todas as transações do banco de dados
    return render(request, 'finance/listar_transacoes.html', {'transacoes': transacoes})

def nova_transacao(request): # esta é uma função padrão que lida com a criação de uma nova transação financeira. Ela processa o formulário enviado pelo usuário e salva os dados no banco de dados.
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Transação adicionada com sucesso!")
    else:
        form = TransacaoForm()
    return render(request, 'finance/nova_transacao.html', {'form': form})
