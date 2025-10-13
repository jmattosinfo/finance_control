# views.py são responsáveis por lidar com as requisições HTTP, processar dados e retornar respostas. 
# Por exemplo, renderizar templates HTML ou retornar dados em formato JSON. JSON são usados para APIs.
# Aqui você define funções ou classes que recebem uma requisição e retornam uma resposta.

from django.shortcuts import render
from django.http import HttpResponse
from .models import Transacao
from .forms import TransacaoForm
from django.shortcuts import render
from datetime import date
from calendar import monthrange

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

def mes_atual (request, ano=None, mes=None):
    # se ano e mes não forem fornecidos, usa o mês e ano atuais
    hoje = date.today()
    if not ano or not mes:
        ano = hoje.year
        mes = hoje.month
    
    # filtra as transações do mês e ano especificados
    transacoes = Transacao.objects.filter(data__year=ano, data__month=mes)
    
    # calcula os totais
    total_entradas = sum(t.valor for t in transacoes if t.categoria == 'receita')
    total_saidas = sum(t.valor for t in transacoes if t.categoria == 'despesa')
    total_guardar = sum(t.valor for t in transacoes if t.categoria == 'guardar')
    
    # define mês anterior e proximo (com ajustes de ano)
    
    if mes == 1: # essa lógica ajusta o ano ao navegar entre dezembro e janeiro
        mes_anterior = 12 # aqui ajusta o mês anterior, usando 12 para dezembro
        ano_anterior = ano - 1 # aqui ajusta o ano anterior, pois -1 representa um ano anterior
    else:
        mes_anterior = mes - 1
        ano_anterior = ano
    
    if mes == 12:
        mes_proximo = 1
        ano_proximo = ano + 1
    else:
        mes_proximo = mes + 1
        ano_proximo = ano
        
    context = {
        "ano": ano,
        "mes": mes,
        "transacoes": transacoes,
        "total_entradas": total_entradas,
        "total_saidas": total_saidas,
        "total_guardar": total_guardar,
        "total_prev_entradas": 0, #valores fixos para o gráfico de barras, usando 0 por enquanto como placeholder
        "total_prev_saidas": 0,
        "total_prev_guardar": 0,
        "mes_anterior": mes_anterior,
        "ano_anterior": ano_anterior,
        "mes_proximo": mes_proximo,
        "ano_proximo": ano_proximo,
    }
    
    return render(request, "finance/mes_atual.html", context)

   