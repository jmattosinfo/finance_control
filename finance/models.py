from django.db import models
from django.contrib.auth.models import User

class Membro(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nome

class Transacao(models.Model):
    CATEGORIAS = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]
    # Aqui usamos o relacionamento com o modelo Membro
    membro = models.ForeignKey(Membro, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField() 
    data_vencimento = models.DateField(null=True, blank=True) 
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    pago = models.BooleanField(default=False)
    
    def __str__(self):
        status = 'Pago' if self.pago else 'Pendente'
        return f"{self.data_vencimento} | {self.descricao}: R$ {self.valor} ({status})"

class Previsao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)
    valor_previsto = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=Transacao.CATEGORIAS)
    mes_referencia = models.IntegerField() 
    ano_referencia = models.IntegerField()

    def __str__(self):
        return f"PREV: {self.descricao} - R$ {self.valor_previsto}"