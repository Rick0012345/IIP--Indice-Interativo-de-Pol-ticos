from django import forms
from .models import Politico, Cargo, Partido
from django.core.exceptions import ValidationError


class PoliticoForm(forms.ModelForm):
    """Formulário para criar e editar políticos"""
    
    class Meta:
        model = Politico
        fields = ['nome', 'cargo', 'partido', 'foto_url']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do político'
            }),
            'cargo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'partido': forms.Select(attrs={
                'class': 'form-select'
            }),
            'foto_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL da foto do político (opcional)'
            }),

        }
        labels = {
            'nome': 'Nome Completo',
            'cargo': 'Cargo',
            'partido': 'Partido',
            'foto_url': 'URL da Foto',

        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Torna alguns campos opcionais na interface
        self.fields['foto_url'].required = False