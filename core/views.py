from django.http import HttpResponse
from finance.models import Transacao
from finance.forms import TransacaoForm
from django.shortcuts import render

from django.shortcuts import redirect

def home(request):
    return render(request, "home.html")

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
