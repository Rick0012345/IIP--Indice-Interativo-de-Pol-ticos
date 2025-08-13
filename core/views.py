from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Avg, Count, Case, When, Value, DecimalField, Q
from django.db import models
from .models import Politico, AvaliacaoUsuario, Nota, Partido, Cargo
from .forms import PoliticoForm

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obter parâmetros de filtro
        partido_filtro = self.request.GET.get('partido')
        cargo_filtro = self.request.GET.get('cargo')
        esfera_filtro = self.request.GET.get('esfera')
        uf_filtro = self.request.GET.get('uf')
        ordenacao = self.request.GET.get('ordenacao', 'pontuacao')  # padrão: ordenar por pontuação
        
        # Query base com anotações para calcular pontuação
        queryset = Politico.objects.select_related('partido', 'cargo').annotate(
            # Média das avaliações dos usuários
            media_usuarios=Avg('avaliacoes__nota'),
            total_avaliacoes=Count('avaliacoes'),
            
            # Nota da IA mais recente
            nota_ia_recente=models.Subquery(
                Nota.objects.filter(politico=models.OuterRef('pk'))
                .order_by('-periodo_ref')
                .values('nota_ia')[:1]
            ),
            
            # Calcular pontuação final (50% usuários + 50% IA)
            pontuacao_final=Case(
                # Se tem ambas as notas
                When(
                    Q(media_usuarios__isnull=False) & Q(nota_ia_recente__isnull=False),
                    then=(models.F('media_usuarios') + models.F('nota_ia_recente')) / 2
                ),
                # Se tem apenas nota dos usuários
                When(
                    Q(media_usuarios__isnull=False) & Q(nota_ia_recente__isnull=True),
                    then=models.F('media_usuarios')
                ),
                # Se tem apenas nota da IA
                When(
                    Q(media_usuarios__isnull=True) & Q(nota_ia_recente__isnull=False),
                    then=models.F('nota_ia_recente')
                ),
                # Se não tem nenhuma nota
                default=Value(0),
                output_field=DecimalField(max_digits=5, decimal_places=2)
            )
        )
        
        # Aplicar filtros
        if partido_filtro:
            queryset = queryset.filter(partido__sigla=partido_filtro)
        if cargo_filtro:
            queryset = queryset.filter(cargo__nome=cargo_filtro)
        if esfera_filtro:
            queryset = queryset.filter(esfera=esfera_filtro)
        if uf_filtro:
            queryset = queryset.filter(uf=uf_filtro)
        
        # Aplicar ordenação
        if ordenacao == 'pontuacao':
            queryset = queryset.order_by('-pontuacao_final', 'nome')
        elif ordenacao == 'nome':
            queryset = queryset.order_by('nome')
        elif ordenacao == 'avaliacoes':
            queryset = queryset.order_by('-total_avaliacoes', '-pontuacao_final')
        
        # Separar por poder e limitar a 10 cada
        context['executivo'] = queryset.filter(cargo__poder='EXECUTIVO')[:10]
        context['legislativo'] = queryset.filter(cargo__poder='LEGISLATIVO')[:10]
        context['judiciario'] = queryset.filter(cargo__poder='JUDICIARIO')[:10]
        
        # Dados para os filtros
        context['partidos'] = Partido.objects.all().order_by('sigla')
        context['cargos'] = Cargo.objects.all().order_by('nome')
        context['esferas'] = Politico.ESFERA_CHOICES
        context['ufs'] = Politico.objects.exclude(uf='').values_list('uf', flat=True).distinct().order_by('uf')
        
        # Valores atuais dos filtros
        context['filtros'] = {
            'partido': partido_filtro,
            'cargo': cargo_filtro,
            'esfera': esfera_filtro,
            'uf': uf_filtro,
            'ordenacao': ordenacao
        }
        
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

def detalhes_politico(request, slug):
    """View para exibir detalhes do político com sistema de avaliação"""
    politico = get_object_or_404(Politico, slug=slug)
    
    # Buscar avaliação do usuário atual (se logado)
    avaliacao_usuario = None
    if request.user.is_authenticated:
        try:
            avaliacao_usuario = AvaliacaoUsuario.objects.get(
                politico=politico, 
                usuario=request.user
            )
        except AvaliacaoUsuario.DoesNotExist:
            pass
    
    # Calcular médias das avaliações
    avaliacoes_stats = AvaliacaoUsuario.objects.filter(politico=politico).aggregate(
        media_usuarios=Avg('nota'),
        total_avaliacoes=Count('id')
    )
    
    # Buscar nota da IA mais recente
    nota_ia_recente = Nota.objects.filter(politico=politico).first()
    nota_ia = nota_ia_recente.nota_ia if nota_ia_recente else None
    
    # Calcular nota final (50% usuários + 50% IA)
    nota_final = None
    if avaliacoes_stats['media_usuarios'] and nota_ia:
        nota_final = (avaliacoes_stats['media_usuarios'] + nota_ia) / 2
    elif avaliacoes_stats['media_usuarios']:
        nota_final = avaliacoes_stats['media_usuarios']
    elif nota_ia:
        nota_final = nota_ia
    
    context = {
        'politico': politico,
        'avaliacao_usuario': avaliacao_usuario,
        'media_usuarios': avaliacoes_stats['media_usuarios'],
        'total_avaliacoes': avaliacoes_stats['total_avaliacoes'],
        'nota_ia': nota_ia,
        'nota_final': nota_final,
    }
    
    return render(request, 'detalhes_politico.html', context)

@login_required
def avaliar_politico(request, slug):
    """View para processar avaliação do usuário via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    politico = get_object_or_404(Politico, slug=slug)
    
    try:
        nota = int(request.POST.get('nota'))
        comentario = request.POST.get('comentario', '').strip()
        
        if not (1 <= nota <= 10):
            return JsonResponse({'error': 'Nota deve estar entre 1 e 10'}, status=400)
        
        # Criar ou atualizar avaliação
        avaliacao, created = AvaliacaoUsuario.objects.update_or_create(
            politico=politico,
            usuario=request.user,
            defaults={
                'nota': nota,
                'comentario': comentario
            }
        )
        
        # Recalcular estatísticas
        avaliacoes_stats = AvaliacaoUsuario.objects.filter(politico=politico).aggregate(
            media_usuarios=Avg('nota'),
            total_avaliacoes=Count('id')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Avaliação salva com sucesso!',
            'media_usuarios': round(avaliacoes_stats['media_usuarios'], 1) if avaliacoes_stats['media_usuarios'] else None,
            'total_avaliacoes': avaliacoes_stats['total_avaliacoes'],
            'created': created
        })
        
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Dados inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Erro interno do servidor'}, status=500)
