from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Bem vindo ao Controle Financeiro! 💰</h1>")

# Create your views here.
