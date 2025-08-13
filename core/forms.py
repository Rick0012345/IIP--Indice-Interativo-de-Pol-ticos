from django import forms
from .models import Politico, Cargo, Partido
from django.core.exceptions import ValidationError


class PoliticoForm(forms.ModelForm):
    """Formulário para criar e editar políticos"""
    
    class Meta:
        model = Politico
        fields = ['nome', 'cargo', 'partido', 'foto', 'foto_url']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Nome completo do político'
            }),
            'cargo': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'partido': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'foto': forms.ClearableFileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'image/*'
            }),
            'foto_url': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'URL da foto do político (opcional)'
            }),
        }
        labels = {
            'nome': 'Nome Completo',
            'cargo': 'Cargo',
            'partido': 'Partido',
            'foto': 'Upload da Foto',
            'foto_url': 'URL da Foto',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Torna alguns campos opcionais na interface
        self.fields['foto'].required = False
        self.fields['foto_url'].required = False