from django.core.management.base import BaseCommand
from core.models import Politico, Partido, Cargo
from django.utils.text import slugify
import requests
from datetime import date


class Command(BaseCommand):
    help = 'Popula o banco de dados com políticos brasileiros de exemplo'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando população de dados...')
        
        # Criar partidos se não existirem
        partidos_data = [
            {'sigla': 'PT', 'nome': 'Partido dos Trabalhadores'},
            {'sigla': 'PL', 'nome': 'Partido Liberal'},
            {'sigla': 'PSDB', 'nome': 'Partido da Social Democracia Brasileira'},
            {'sigla': 'MDB', 'nome': 'Movimento Democrático Brasileiro'},
            {'sigla': 'PP', 'nome': 'Progressistas'},
            {'sigla': 'PDT', 'nome': 'Partido Democrático Trabalhista'},
            {'sigla': 'PSB', 'nome': 'Partido Socialista Brasileiro'},
            {'sigla': 'REPUBLICANOS', 'nome': 'Republicanos'},
            {'sigla': 'UNIÃO', 'nome': 'União Brasil'},
            {'sigla': 'PSD', 'nome': 'Partido Social Democrático'},
        ]
        
        for partido_info in partidos_data:
            partido, created = Partido.objects.get_or_create(
                sigla=partido_info['sigla'],
                defaults={'nome': partido_info['nome']}
            )
            if created:
                self.stdout.write(f'Partido criado: {partido.sigla}')
        
        # Criar cargos se não existirem
        cargos_data = [
            {'nome': 'Presidente da República', 'poder': 'EXECUTIVO', 'nivel': 'FEDERAL'},
            {'nome': 'Governador', 'poder': 'EXECUTIVO', 'nivel': 'ESTADUAL'},
            {'nome': 'Prefeito', 'poder': 'EXECUTIVO', 'nivel': 'MUNICIPAL'},
            {'nome': 'Senador', 'poder': 'LEGISLATIVO', 'nivel': 'FEDERAL'},
            {'nome': 'Deputado Federal', 'poder': 'LEGISLATIVO', 'nivel': 'FEDERAL'},
            {'nome': 'Deputado Estadual', 'poder': 'LEGISLATIVO', 'nivel': 'ESTADUAL'},
            {'nome': 'Vereador', 'poder': 'LEGISLATIVO', 'nivel': 'MUNICIPAL'},
            {'nome': 'Ministro do STF', 'poder': 'JUDICIARIO', 'nivel': 'FEDERAL'},
        ]
        
        for cargo_info in cargos_data:
            cargo, created = Cargo.objects.get_or_create(
                nome=cargo_info['nome'],
                poder=cargo_info['poder'],
                nivel=cargo_info['nivel']
            )
            if created:
                self.stdout.write(f'Cargo criado: {cargo.nome}')
        
        # Dados de políticos brasileiros conhecidos
        politicos_data = [
            # Executivo Federal
            {
                'nome': 'Luiz Inácio Lula da Silva',
                'partido': 'PT',
                'cargo': 'Presidente da República',
                'uf': 'DF',
                'municipio': 'Brasília',
                'esfera': 'FEDERAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Lula_-_foto_oficial05012023_%28cropped%29.jpg/256px-Lula_-_foto_oficial05012023_%28cropped%29.jpg',
                'data_nascimento': date(1945, 10, 27)
            },
            # Executivo Estadual
            {
                'nome': 'Tarcísio Gomes de Freitas',
                'partido': 'REPUBLICANOS',
                'cargo': 'Governador',
                'uf': 'SP',
                'municipio': 'São Paulo',
                'esfera': 'ESTADUAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Tarcisio_Gomes_de_Freitas_em_2023.jpg/256px-Tarcisio_Gomes_de_Freitas_em_2023.jpg',
                'data_nascimento': date(1975, 7, 12)
            },
            {
                'nome': 'Cláudio Castro',
                'partido': 'PL',
                'cargo': 'Governador',
                'uf': 'RJ',
                'municipio': 'Rio de Janeiro',
                'esfera': 'ESTADUAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Cl%C3%A1udio_Castro_em_2021.jpg/256px-Cl%C3%A1udio_Castro_em_2021.jpg',
                'data_nascimento': date(1979, 2, 6)
            },
            # Executivo Municipal
            {
                'nome': 'Ricardo Nunes',
                'partido': 'MDB',
                'cargo': 'Prefeito',
                'uf': 'SP',
                'municipio': 'São Paulo',
                'esfera': 'MUNICIPAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Ricardo_Nunes_em_2021.jpg/256px-Ricardo_Nunes_em_2021.jpg',
                'data_nascimento': date(1967, 8, 7)
            },
            {
                'nome': 'Eduardo Paes',
                'partido': 'PSD',
                'cargo': 'Prefeito',
                'uf': 'RJ',
                'municipio': 'Rio de Janeiro',
                'esfera': 'MUNICIPAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Eduardo_Paes_em_2021.jpg/256px-Eduardo_Paes_em_2021.jpg',
                'data_nascimento': date(1969, 11, 14)
            },
            # Legislativo Federal
            {
                'nome': 'Arthur Lira',
                'partido': 'PP',
                'cargo': 'Deputado Federal',
                'uf': 'AL',
                'municipio': 'Maceió',
                'esfera': 'FEDERAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Arthur_Lira_em_2021.jpg/256px-Arthur_Lira_em_2021.jpg',
                'data_nascimento': date(1969, 9, 25)
            },
            {
                'nome': 'Rodrigo Pacheco',
                'partido': 'PSD',
                'cargo': 'Senador',
                'uf': 'MG',
                'municipio': 'Belo Horizonte',
                'esfera': 'FEDERAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Rodrigo_Pacheco_em_2021.jpg/256px-Rodrigo_Pacheco_em_2021.jpg',
                'data_nascimento': date(1976, 7, 31)
            },
            {
                'nome': 'Gleisi Hoffmann',
                'partido': 'PT',
                'cargo': 'Deputado Federal',
                'uf': 'PR',
                'municipio': 'Curitiba',
                'esfera': 'FEDERAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Gleisi_Hoffmann_em_2019.jpg/256px-Gleisi_Hoffmann_em_2019.jpg',
                'data_nascimento': date(1965, 1, 6)
            },
            {
                'nome': 'Marcelo Freixo',
                'partido': 'PSB',
                'cargo': 'Deputado Federal',
                'uf': 'RJ',
                'municipio': 'Rio de Janeiro',
                'esfera': 'FEDERAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Marcelo_Freixo_em_2018.jpg/256px-Marcelo_Freixo_em_2018.jpg',
                'data_nascimento': date(1967, 9, 12)
            },
            # Judiciário
            {
                'nome': 'Luís Roberto Barroso',
                'partido': None,
                'cargo': 'Ministro do STF',
                'uf': 'DF',
                'municipio': 'Brasília',
                'esfera': 'FEDERAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Lu%C3%ADs_Roberto_Barroso_em_2021.jpg/256px-Lu%C3%ADs_Roberto_Barroso_em_2021.jpg',
                'data_nascimento': date(1958, 3, 11)
            },
            {
                'nome': 'Alexandre de Moraes',
                'partido': None,
                'cargo': 'Ministro do STF',
                'uf': 'DF',
                'municipio': 'Brasília',
                'esfera': 'FEDERAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Alexandre_de_Moraes_em_2021.jpg/256px-Alexandre_de_Moraes_em_2021.jpg',
                'data_nascimento': date(1968, 12, 13)
            },
        ]
        
        # Criar políticos
        for politico_info in politicos_data:
            # Buscar partido se especificado
            partido = None
            if politico_info['partido']:
                try:
                    partido = Partido.objects.get(sigla=politico_info['partido'])
                except Partido.DoesNotExist:
                    self.stdout.write(f"Partido {politico_info['partido']} não encontrado")
            
            # Buscar cargo
            try:
                cargo = Cargo.objects.get(nome=politico_info['cargo'])
            except Cargo.DoesNotExist:
                self.stdout.write(f"Cargo {politico_info['cargo']} não encontrado")
                continue
            
            # Criar slug único
            base_slug = slugify(politico_info['nome'])
            slug = base_slug
            counter = 1
            while Politico.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            # Criar ou atualizar político
            politico, created = Politico.objects.get_or_create(
                nome=politico_info['nome'],
                defaults={
                    'slug': slug,
                    'partido': partido,
                    'cargo': cargo,
                    'uf': politico_info['uf'],
                    'municipio': politico_info['municipio'],
                    'esfera': politico_info['esfera'],
                    'foto_url': politico_info['foto_url'],
                    'data_nascimento': politico_info['data_nascimento'],
                    'ativo': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Político criado: {politico.nome} - {cargo.nome}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Político já existe: {politico.nome}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('População de dados concluída com sucesso!')
        )
        
        # Estatísticas finais
        total_politicos = Politico.objects.count()
        total_partidos = Partido.objects.count()
        total_cargos = Cargo.objects.count()
        
        self.stdout.write(f'\nEstatísticas:')
        self.stdout.write(f'- Total de políticos: {total_politicos}')
        self.stdout.write(f'- Total de partidos: {total_partidos}')
        self.stdout.write(f'- Total de cargos: {total_cargos}')