from django.http import HttpResponse
from finance.models import Transacao
from finance.forms import TransacaoForm
from django.shortcuts import render

from django.shortcuts import redirect

#ajustar home para exibir transações
def home(request):
    Transacao.objects.all()
    
    return render(request, "finance/home.html", {"transacoes": Transacao}) #ajustar para exibir transações

def sobre(request): #request é o objeto que contém todas as informações sobre a requisição HTTP feita pelo cliente
    return render(request, "finance/sobre.html") #o render substitui o HttpResponse, facilitando a renderização de templates

def listar_transacoes(request):
    return render(request, "listar_transacoes.html")


def nova_transacao(request):
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_transacoes')
    else:
        form = TransacaoForm()
        
    return render(request, 'finance/nova_transacao.html', {'form': form})
