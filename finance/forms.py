from django import forms
from .models import Transacao # Importa o modelo Transacao para criar um formulário baseado nele
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao # Especifica que este formulário é baseado no modelo Transacao
        fields = ['descricao', 'valor', 'data', 'categoria', 'pago'] # Define os campos que estarão presentes no formulário
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Salário, Aluguel, etc.'}), # Define o estilo e o placeholder do campo de descrição
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1000.00'}), # Define o estilo e o placeholder do campo de valor
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), # Define o estilo e o tipo do campo de data
            'categoria': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Ex: Receita, Despesa'}), 
            'pago': forms.CheckboxInput(attrs={'class': 'form-check-input'}), # Define o estilo
        }
class CadastroForm(UserCreationForm):
        
        # email = forms.EmailField(
        #     required=True, 
        #     widget=forms.EmailInput(
        #         attrs={                  
        #             'placeholder': 'Email'
        #                }
        #         )
        # )
            
    class Meta: #class Meta define metadados para o formulário, fazendo a ligação com o modelo User do Django.
            model = User
            fields = ['username', 'password1', 'password2']
            
            help_texts = {
            'username': None,
            # 'email': None,
            'password1': None,
            'password2': None,
        }
        
            

               
    def __init__(self, *args, **kwargs):
        super(CadastroForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'}) #adiciona a classe CSS 'form-control' a todos os campos do formulário
                

                
            self.fields['username'].widget.attrs['placeholder'] = 'Nome de usuário'
            self.fields['password1'].widget.attrs['placeholder'] = 'Crie uma senha'
            self.fields['password2'].widget.attrs['placeholder'] = 'Confirme a senha'
            
        
        