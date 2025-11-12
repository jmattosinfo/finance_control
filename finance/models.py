from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#models.py servem para definir a estrutura do banco de dados, criando tabelas e campos.
# para começar a criar modelos, você deve importar models do django.db e criar classes que herdam de models.Model.

#criar um modelo de transação financeira como exemplo que contenha descrição, valor, data e categoria (receita ou despesa).

class Transacao(models.Model): #models.Model herda da classe Model do Django
    CATEGORIAS = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100) #CharField é um campo de texto com tamanho máximo definido
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    pago = models.BooleanField(default=False) #BooleanField é um campo que armazena valores True ou False
    
    
    def __str__(self):
        return f"{self.descricao} - {self.valor} - {self.data} - {self.categoria} - {'Pago' if self.pago else 'Não Pago'}"

    #__str__ define a representação em string do objeto, útil para exibição no administrador do Django.
    # self refere-se à instância atual do modelo que esta sendo manipulada.