from django import forms
from allauth.account.forms import SignupForm
from .models import CustomUser
import re
from datetime import date
from django.core.exceptions import ValidationError


class CustomSignupForm(SignupForm):
    """Formulário customizado de registro com CPF"""
    
    cpf = forms.CharField(
        max_length=14,
        label='CPF',
        help_text='Digite apenas os números do CPF',
        widget=forms.TextInput(attrs={
            'placeholder': '000.000.000-00',
            'class': 'form-control',
            'pattern': '[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}|[0-9]{11}'
        })
    )
    
    nome_completo = forms.CharField(
        max_length=255,
        label='Nome Completo',
        widget=forms.TextInput(attrs={
            'placeholder': 'Seu nome completo',
            'class': 'form-control'
        })
    )
    
    telefone = forms.CharField(
        max_length=20,
        label='Telefone',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '(11) 99999-9999',
            'class': 'form-control'
        })
    )
    
    data_nascimento = forms.DateField(
        label='Data de Nascimento',
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    def clean_cpf(self):
        """Valida e limpa o CPF"""
        cpf = self.cleaned_data.get('cpf', '')
        
        # Remove caracteres não numéricos
        cpf_clean = re.sub(r'\D', '', cpf)
        
        if len(cpf_clean) != 11:
            raise forms.ValidationError('CPF deve ter 11 dígitos.')
        
        # Verifica se todos os dígitos são iguais (CPF inválido)
        if cpf_clean == cpf_clean[0] * 11:
            raise forms.ValidationError('CPF inválido.')
        
        # Verifica se CPF já existe
        if CustomUser.objects.filter(cpf=cpf_clean).exists():
            raise forms.ValidationError('Já existe um usuário cadastrado com este CPF.')
        
        return cpf_clean
    
    def clean_data_nascimento(self):
        """Valida se o usuário tem pelo menos 16 anos"""
        from datetime import date
        
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if data_nascimento:
            hoje = date.today()
            idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
            
            if idade < 16:
                raise forms.ValidationError('Você deve ter pelo menos 16 anos para se cadastrar.')
        
        return data_nascimento
    
    def clean_nome_completo(self):
        """Valida o nome completo"""
        nome_completo = self.cleaned_data.get('nome_completo')
        if nome_completo and len(nome_completo.strip()) < 2:
            raise forms.ValidationError('Nome completo deve ter pelo menos 2 caracteres.')
        return nome_completo
    
    def clean_data_nascimento(self):
        """Valida se o usuário tem pelo menos 18 anos"""
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if data_nascimento:
            hoje = date.today()
            idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
            
            if idade < 18:
                raise ValidationError('Você deve ter pelo menos 18 anos para criar uma conta.')
        
        return data_nascimento
    
    def save(self, request):
        """Salva o usuário com os campos customizados"""
        user = super().save(request)
        
        # Adiciona os campos customizados
        user.cpf = self.cleaned_data.get('cpf')
        user.nome_completo = self.cleaned_data.get('nome_completo')
        user.telefone = self.cleaned_data.get('telefone', '')
        user.data_nascimento = self.cleaned_data.get('data_nascimento')
        
        user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customiza os campos padrão
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nome de usuário'
        })
        
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'seu@email.com'
        })
        
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Senha'
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirme a senha'
        })
        
        # Reordena os campos
        field_order = ['nome_completo', 'cpf', 'username', 'email', 'telefone', 'data_nascimento', 'password1', 'password2']
        self.order_fields(field_order)