from django import forms
from .models import Transacao # Importa o modelo Transacao para criar um formulário baseado nele

class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['descricao', 'valor', 'data', 'categoria', 'pago']
        