from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Politico

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Carregar até 10 políticos por poder (pode ajustar depois para ranking real)
        context['exec_politicos'] = (
            Politico.objects.select_related('partido', 'cargo')
            .filter(cargo__poder='EXECUTIVO')[:10]
        )
        context['leg_politicos'] = (
            Politico.objects.select_related('partido', 'cargo')
            .filter(cargo__poder='LEGISLATIVO')[:10]
        )
        context['jud_politicos'] = (
            Politico.objects.select_related('partido', 'cargo')
            .filter(cargo__poder='JUDICIARIO')[:10]
        )
        
        return context

# Create your views here.
