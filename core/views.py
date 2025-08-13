from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from .models import Politico
from .forms import PoliticoForm

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Carrega até 10 políticos de cada poder
        context['executivo'] = Politico.objects.filter(
            cargo__poder='EXECUTIVO'
        )[:10]
        
        context['legislativo'] = Politico.objects.filter(
            cargo__poder='LEGISLATIVO'
        )[:10]
        
        context['judiciario'] = Politico.objects.filter(
            cargo__poder='JUDICIARIO'
        )[:10]
        
        return context

def gerenciar_politico(request, politico_id=None):
    """View para gerenciar (criar/editar) políticos"""
    if politico_id:
        politico = get_object_or_404(Politico, id=politico_id)
        titulo = f'Editar {politico.nome}'
    else:
        politico = None
        titulo = 'Adicionar Novo Político'
    
    if request.method == 'POST':
        form = PoliticoForm(request.POST, instance=politico)
        if form.is_valid():
            politico_salvo = form.save()
            if politico_id:
                messages.success(request, f'Político {politico_salvo.nome} atualizado com sucesso!')
            else:
                messages.success(request, f'Político {politico_salvo.nome} criado com sucesso!')
            return redirect('home')
    else:
        form = PoliticoForm(instance=politico)
    
    return render(request, 'gerenciar_politico.html', {
        'form': form,
        'politico': politico,
        'titulo': titulo
    })

def deletar_politico(request, politico_id):
    """View para deletar um político"""
    politico = get_object_or_404(Politico, id=politico_id)
    
    if request.method == 'POST':
        nome = politico.nome
        politico.delete()
        messages.success(request, f'Político {nome} removido com sucesso!')
        return redirect('home')
    
    return render(request, 'confirmar_delete.html', {'politico': politico})

# Create your views here.
