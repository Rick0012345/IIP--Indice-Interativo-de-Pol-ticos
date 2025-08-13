from django.core.management.base import BaseCommand
from core.models import Politico
import requests
from urllib.parse import urlparse

class Command(BaseCommand):
    help = 'Atualiza as fotos dos políticos com URLs mais confiáveis'

    def handle(self, *args, **options):
        self.stdout.write('Atualizando fotos dos políticos...')
        
        # Cores para diferentes tipos de políticos
        cores_por_poder = {
            'EXECUTIVO': '4F46E5',  # Roxo
            'LEGISLATIVO': '059669', # Verde
            'JUDICIARIO': 'DC2626'   # Vermelho
        }
        
        cores_por_cargo = {
            'Presidente': 'FFD700',
            'Vice-Presidente': 'FFA500', 
            'Governador': '4F46E5',
            'Prefeito': '3B82F6',
            'Ministro': '8B5CF6',
            'Deputado Federal': '059669',
            'Senador': '10B981',
            'Ministro do STF': 'DC2626'
        }
        
        # Atualizar fotos dos políticos
        politicos_atualizados = 0
        
        for politico in Politico.objects.all():
            # Determinar cor baseada no cargo ou poder
            cargo_nome = politico.cargo.nome if politico.cargo else 'Político'
            cor = cores_por_cargo.get(cargo_nome, cores_por_poder.get(politico.esfera, '6B7280'))
            
            # Criar iniciais do nome
            nomes = politico.nome.split()
            if len(nomes) >= 2:
                iniciais = f'{nomes[0][0]}{nomes[-1][0]}'
            else:
                iniciais = nomes[0][:2] if nomes else 'P'
            
            # Simplesmente limpar as fotos problemáticas
            # Deixar o campo vazio para usar o fallback do template
            nova_url = ''
            
            # Atualizar apenas se a URL for diferente
            if politico.foto_url != nova_url:
                politico.foto_url = nova_url
                politico.save()
                politicos_atualizados += 1
                self.stdout.write(f'✓ Foto removida: {politico.nome} (usará fallback)')
            else:
                self.stdout.write(f'- Já sem foto: {politico.nome}')
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(f'Atualização de fotos concluída!')
        self.stdout.write(f'- Políticos com fotos atualizadas: {politicos_atualizados}')
        self.stdout.write(f'- Total de políticos: {Politico.objects.count()}')
        self.stdout.write('='*60)