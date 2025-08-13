from django.core.management.base import BaseCommand
from core.models import Politico, Partido, Cargo
from django.utils.text import slugify
from datetime import date


class Command(BaseCommand):
    help = 'Adiciona mais políticos brasileiros conhecidos ao banco de dados'

    def handle(self, *args, **options):
        self.stdout.write('Adicionando mais políticos...')
        
        # Garantir que os cargos existem
        cargos_data = [
            {'nome': 'Vice-Presidente da República', 'poder': 'EXECUTIVO', 'nivel': 'FEDERAL'},
            {'nome': 'Ministro', 'poder': 'EXECUTIVO', 'nivel': 'FEDERAL'},
        ]
        
        for cargo_info in cargos_data:
            cargo, created = Cargo.objects.get_or_create(
                nome=cargo_info['nome'],
                poder=cargo_info['poder'],
                nivel=cargo_info['nivel']
            )
            if created:
                self.stdout.write(f'Cargo criado: {cargo.nome}')
        
        # Mais políticos brasileiros conhecidos
        politicos_data = [
            # Executivo Federal - Ministros
            {
                'nome': 'Geraldo Alckmin',
                'partido': 'PSB',
                'cargo': 'Vice-Presidente da República',
                'uf': 'DF',
                'municipio': 'Brasília',
                'esfera': 'FEDERAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Geraldo_Alckmin_em_2022.jpg/256px-Geraldo_Alckmin_em_2022.jpg',
                'data_nascimento': date(1952, 11, 7)
            },
            {
                'nome': 'Fernando Haddad',
                'partido': 'PT',
                'cargo': 'Ministro',
                'uf': 'DF',
                'municipio': 'Brasília',
                'esfera': 'FEDERAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Fernando_Haddad_em_2022.jpg/256px-Fernando_Haddad_em_2022.jpg',
                'data_nascimento': date(1963, 1, 25)
            },
            {
                'nome': 'Flávio Dino',
                'partido': 'PSB',
                'cargo': 'Ministro',
                'uf': 'DF',
                'municipio': 'Brasília',
                'esfera': 'FEDERAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Fl%C3%A1vio_Dino_em_2022.jpg/256px-Fl%C3%A1vio_Dino_em_2022.jpg',
                'data_nascimento': date(1968, 5, 16)
            },
            # Mais Governadores
            {
                'nome': 'Romeu Zema',
                'partido': 'UNIÃO',
                'cargo': 'Governador',
                'uf': 'MG',
                'municipio': 'Belo Horizonte',
                'esfera': 'ESTADUAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Romeu_Zema_em_2022.jpg/256px-Romeu_Zema_em_2022.jpg',
                'data_nascimento': date(1964, 11, 28)
            },
            {
                'nome': 'Ratinho Junior',
                'partido': 'PSD',
                'cargo': 'Governador',
                'uf': 'PR',
                'municipio': 'Curitiba',
                'esfera': 'ESTADUAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Ratinho_Junior_em_2022.jpg/256px-Ratinho_Junior_em_2022.jpg',
                'data_nascimento': date(1981, 10, 29)
            },
            {
                'nome': 'Eduardo Leite',
                'partido': 'PSDB',
                'cargo': 'Governador',
                'uf': 'RS',
                'municipio': 'Porto Alegre',
                'esfera': 'ESTADUAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Eduardo_Leite_em_2022.jpg/256px-Eduardo_Leite_em_2022.jpg',
                'data_nascimento': date(1985, 3, 10)
            },
            # Mais Prefeitos
            {
                'nome': 'João Doria',
                'partido': 'PSDB',
                'cargo': 'Prefeito',
                'uf': 'SP',
                'municipio': 'São Paulo',
                'esfera': 'MUNICIPAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Jo%C3%A3o_Doria_em_2021.jpg/256px-Jo%C3%A3o_Doria_em_2021.jpg',
                'data_nascimento': date(1957, 12, 16)
            },
            {
                'nome': 'Bruno Covas',
                'partido': 'PSDB',
                'cargo': 'Prefeito',
                'uf': 'SP',
                'municipio': 'São Paulo',
                'esfera': 'MUNICIPAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Bruno_Covas_em_2020.jpg/256px-Bruno_Covas_em_2020.jpg',
                'data_nascimento': date(1980, 4, 7)
            },
            # Deputados Federais conhecidos
            {
                'nome': 'Jair Bolsonaro',
                'partido': 'PL',
                'cargo': 'Deputado Federal',
                'uf': 'RJ',
                'municipio': 'Rio de Janeiro',
                'esfera': 'FEDERAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Jair_Bolsonaro_em_2022.jpg/256px-Jair_Bolsonaro_em_2022.jpg',
                'data_nascimento': date(1955, 3, 21)
            },
            {
                'nome': 'Tabata Amaral',
                'partido': 'PSB',
                'cargo': 'Deputado Federal',
                'uf': 'SP',
                'municipio': 'São Paulo',
                'esfera': 'FEDERAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/t/t4/Tabata_Amaral_em_2022.jpg/256px-Tabata_Amaral_em_2022.jpg',
                'data_nascimento': date(1993, 11, 14)
            },
            {
                'nome': 'Kim Kataguiri',
                'partido': 'UNIÃO',
                'cargo': 'Deputado Federal',
                'uf': 'SP',
                'municipio': 'São Paulo',
                'esfera': 'FEDERAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/k/k4/Kim_Kataguiri_em_2022.jpg/256px-Kim_Kataguiri_em_2022.jpg',
                'data_nascimento': date(1996, 1, 28)
            },
            {
                'nome': 'Carla Zambelli',
                'partido': 'PL',
                'cargo': 'Deputado Federal',
                'uf': 'SP',
                'municipio': 'São Paulo',
                'esfera': 'FEDERAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Carla_Zambelli_em_2022.jpg/256px-Carla_Zambelli_em_2022.jpg',
                'data_nascimento': date(1978, 8, 28)
            },
            # Senadores
            {
                'nome': 'Flávio Bolsonaro',
                'partido': 'PL',
                'cargo': 'Senador',
                'uf': 'RJ',
                'municipio': 'Rio de Janeiro',
                'esfera': 'FEDERAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Fl%C3%A1vio_Bolsonaro_em_2022.jpg/256px-Fl%C3%A1vio_Bolsonaro_em_2022.jpg',
                'data_nascimento': date(1981, 4, 30)
            },
            {
                'nome': 'Simone Tebet',
                'partido': 'MDB',
                'cargo': 'Senador',
                'uf': 'MS',
                'municipio': 'Campo Grande',
                'esfera': 'FEDERAL',
                'foto_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/s/s4/Simone_Tebet_em_2022.jpg/256px-Simone_Tebet_em_2022.jpg',
                'data_nascimento': date(1970, 1, 21)
            },
        ]
        
        # Criar políticos
        importados = 0
        ja_existem = 0
        
        for politico_info in politicos_data:
            # Buscar partido se especificado
            partido = None
            if politico_info['partido']:
                try:
                    partido = Partido.objects.get(sigla=politico_info['partido'])
                except Partido.DoesNotExist:
                    # Criar partido se não existir
                    partido = Partido.objects.create(
                        sigla=politico_info['partido'],
                        nome=politico_info['partido']
                    )
                    self.stdout.write(f"Partido criado: {partido.sigla}")
            
            # Buscar cargo
            try:
                cargo = Cargo.objects.get(nome=politico_info['cargo'])
            except Cargo.DoesNotExist:
                self.stdout.write(f"Cargo {politico_info['cargo']} não encontrado")
                continue
            
            # Verificar se já existe
            if Politico.objects.filter(nome=politico_info['nome']).exists():
                ja_existem += 1
                self.stdout.write(
                    self.style.WARNING(f'Já existe: {politico_info["nome"]}')
                )
                continue
            
            # Criar slug único
            base_slug = slugify(politico_info['nome'])
            slug = base_slug
            counter = 1
            while Politico.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            # Criar político
            politico = Politico.objects.create(
                nome=politico_info['nome'],
                slug=slug,
                partido=partido,
                cargo=cargo,
                uf=politico_info['uf'],
                municipio=politico_info['municipio'],
                esfera=politico_info['esfera'],
                foto_url=politico_info['foto_url'],
                data_nascimento=politico_info['data_nascimento'],
                ativo=True
            )
            
            importados += 1
            self.stdout.write(
                self.style.SUCCESS(f'✓ Criado: {politico.nome} - {cargo.nome} ({politico_info["partido"]}/{politico_info["uf"]})')
            )
        
        # Estatísticas finais
        self.stdout.write('\n' + '='*60)
        self.stdout.write(
            self.style.SUCCESS('Adição de políticos concluída!')
        )
        self.stdout.write(f'- Novos políticos adicionados: {importados}')
        self.stdout.write(f'- Políticos que já existiam: {ja_existem}')
        self.stdout.write(f'- Total de políticos no banco: {Politico.objects.count()}')
        
        # Estatísticas por poder
        exec_count = Politico.objects.filter(cargo__poder='EXECUTIVO').count()
        leg_count = Politico.objects.filter(cargo__poder='LEGISLATIVO').count()
        jud_count = Politico.objects.filter(cargo__poder='JUDICIARIO').count()
        
        self.stdout.write('\nDistribuição por poder:')
        self.stdout.write(f'- Executivo: {exec_count} políticos')
        self.stdout.write(f'- Legislativo: {leg_count} políticos')
        self.stdout.write(f'- Judiciário: {jud_count} políticos')