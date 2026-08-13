from django import forms
from .models import Transacao # Importa o modelo Transacao para criar um formulário baseado nele
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Membro

class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['descricao', 'valor', 'data', 'data_vencimento', 'categoria', 'membro', 'pago'] 
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Salário, Aluguel, etc.'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1000.00'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'membro': forms.Select(attrs={'class': 'form-control'}),
            'pago': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(TransacaoForm, self).__init__(*args, **kwargs)
        # Filtra para mostrar apenas os membros (JC, KW...) deste usuário específico
        self.fields['membro'].queryset = Membro.objects.filter(user=user)
        self.fields['membro'].empty_label = "Selecione o Responsável"
        
class MembroForm(forms.ModelForm):
    class Meta:
        model = Membro
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: JC, KW, Filho...'})
        }


class CadastroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email'
            }
        )
    )

    class Meta:  # class Meta define metadados para o formulário, fazendo a ligação com o modelo User do Django.
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }

    def __init__(self, *args, **kwargs):
        super(CadastroForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})  # adiciona a classe CSS 'form-control' a todos os campos

        self.fields['username'].widget.attrs['placeholder'] = 'Nome de usuário'
        self.fields['password1'].widget.attrs['placeholder'] = 'Crie uma senha'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirme a senha'
class EditarContaForm(PasswordChangeForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome de usuário'
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'old_password',
            'new_password1',
            'new_password2'
        ]

    def __init__(self, user, *args, **kwargs):
        

        # Importante: passa "user" como primeiro argumento para o PasswordChangeForm
        super().__init__(user, *args, **kwargs)

        # Preenche username/email
        self.fields['username'].initial = user.username
        self.fields['email'].initial = user.email

        # Aplica classes CSS
        for field in ['old_password', 'new_password1', 'new_password2']:
            self.fields[field].widget.attrs.update({'class': 'form-control'})