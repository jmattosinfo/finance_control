from django import forms
from .models import Transacao # Importa o modelo Transacao para criar um formulário baseado nele

class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao # Especifica que este formulário é baseado no modelo Transacao
        fields = ['descricao', 'valor', 'data', 'categoria', 'pago']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Salário, Aluguel, etc.'}), # Define o estilo e o placeholder do campo de descrição
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1000.00'}), # Define o estilo e o placeholder do campo de valor
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), # Define o estilo e o tipo do campo de data
            'categoria': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Ex: Receita, Despesa'}), 
            'pago': forms.CheckboxInput(attrs={'class': 'form-check-input'}), # Define o estilo
        }
        