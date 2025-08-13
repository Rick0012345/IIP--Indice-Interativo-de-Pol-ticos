from django.core.management.base import BaseCommand
from core.models import Politico, Partido, Cargo
from django.utils.text import slugify
import requests
import time
from datetime import datetime


class Command(BaseCommand):
    help = 'Importa dados de deputados federais da API da Câmara dos Deputados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limite',
            type=int,
            default=20,
            help='Número máximo de deputados para importar (padrão: 20)'
        )

    def handle(self, *args, **options):
        limite = options['limite']
        self.stdout.write(f'Iniciando importação de até {limite} deputados...')
        
        # Garantir que o cargo existe
        cargo_deputado, created = Cargo.objects.get_or_create(
            nome='Deputado Federal',
            poder='LEGISLATIVO',
            nivel='FEDERAL'
        )
        
        try:
            # Buscar lista de deputados da API da Câmara
            url = 'https://dadosabertos.camara.leg.br/api/v2/deputados'
            params = {
                'ordem': 'ASC',
                'ordenarPor': 'nome',
                'itens': limite
            }
            
            self.stdout.write('Fazendo requisição para API da Câmara dos Deputados...')
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            deputados = data.get('dados', [])
            
            self.stdout.write(f'Encontrados {len(deputados)} deputados na API')
            
            importados = 0
            atualizados = 0
            
            for deputado_data in deputados:
                try:
                    # Dados básicos do deputado
                    nome = deputado_data.get('nome', '').strip()
                    if not nome:
                        continue
                    
                    id_deputado = deputado_data.get('id')
                    uf = deputado_data.get('siglaUf', '').upper()
                    partido_sigla = deputado_data.get('siglaPartido', '').upper()
                    
                    # Buscar dados detalhados do deputado
                    detalhes_url = f'https://dadosabertos.camara.leg.br/api/v2/deputados/{id_deputado}'
                    
                    self.stdout.write(f'Buscando detalhes de {nome}...')
                    detalhes_response = requests.get(detalhes_url, timeout=30)
                    
                    if detalhes_response.status_code == 200:
                        detalhes_data = detalhes_response.json().get('dados', {})
                        
                        # Dados adicionais
                        data_nascimento_str = detalhes_data.get('dataNascimento')
                        data_nascimento = None
                        if data_nascimento_str:
                            try:
                                data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
                            except ValueError:
                                pass
                        
                        municipio_nascimento = detalhes_data.get('municipioNascimento', '')
                        foto_url = detalhes_data.get('urlFoto')
                        
                        # Criar ou buscar partido
                        partido = None
                        if partido_sigla:
                            partido, created = Partido.objects.get_or_create(
                                sigla=partido_sigla,
                                defaults={'nome': partido_sigla}  # Nome será atualizado depois se necessário
                            )
                        
                        # Criar slug único
                        base_slug = slugify(nome)
                        slug = base_slug
                        counter = 1
                        while Politico.objects.filter(slug=slug).exists():
                            slug = f"{base_slug}-{counter}"
                            counter += 1
                        
                        # Criar ou atualizar político
                        politico, created = Politico.objects.get_or_create(
                            nome=nome,
                            defaults={
                                'slug': slug,
                                'partido': partido,
                                'cargo': cargo_deputado,
                                'uf': uf,
                                'municipio': municipio_nascimento,
                                'esfera': 'FEDERAL',
                                'foto_url': foto_url,
                                'data_nascimento': data_nascimento,
                                'ativo': True
                            }
                        )
                        
                        if created:
                            importados += 1
                            self.stdout.write(
                                self.style.SUCCESS(f'✓ Importado: {nome} ({partido_sigla}/{uf})')
                            )
                        else:
                            # Atualizar dados se necessário
                            updated = False
                            if politico.partido != partido:
                                politico.partido = partido
                                updated = True
                            if politico.uf != uf:
                                politico.uf = uf
                                updated = True
                            if foto_url and politico.foto_url != foto_url:
                                politico.foto_url = foto_url
                                updated = True
                            if data_nascimento and politico.data_nascimento != data_nascimento:
                                politico.data_nascimento = data_nascimento
                                updated = True
                            
                            if updated:
                                politico.save()
                                atualizados += 1
                                self.stdout.write(
                                    self.style.WARNING(f'↻ Atualizado: {nome} ({partido_sigla}/{uf})')
                                )
                            else:
                                self.stdout.write(
                                    self.style.HTTP_INFO(f'- Já existe: {nome} ({partido_sigla}/{uf})')
                                )
                    
                    # Pausa para não sobrecarregar a API
                    time.sleep(0.5)
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Erro ao processar {nome}: {str(e)}')
                    )
                    continue
            
            # Estatísticas finais
            self.stdout.write('\n' + '='*50)
            self.stdout.write(
                self.style.SUCCESS(f'Importação concluída!')
            )
            self.stdout.write(f'- Deputados importados: {importados}')
            self.stdout.write(f'- Deputados atualizados: {atualizados}')
            self.stdout.write(f'- Total de políticos no banco: {Politico.objects.count()}')
            
        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Erro na requisição à API: {str(e)}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro inesperado: {str(e)}')
            )