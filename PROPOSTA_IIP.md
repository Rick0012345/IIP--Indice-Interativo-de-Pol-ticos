# Índice Interativo de Políticos (IIP) — Proposta de Software

Versão: 0.1 (rascunho inicial)
Responsável: Equipe IIP
Última atualização: [preencher]

1. Objetivo
- Construir um sistema web que ranqueie políticos brasileiros com base em:
  - Dados objetivos oficiais (composição da nota de IA).
  - Análise automatizada de notícias usando IA (composição da nota de IA).
  - Avaliações dos usuários (metade da nota final).
- Garantir transparência, segurança contra manipulação e personalização de filtros para o usuário final.

2. Metodologia de Ranqueamento
- Fórmulas
  - Nota_Final = (Peso_IA × Nota_IA) + (Peso_Usuário × Nota_Usuário)
    - Sugestão inicial: Peso_IA = 0,5 e Peso_Usuário = 0,5 (ajustável por configuração e/ou modo “customizar ranking”).
  - Nota_IA = (Peso_Objetivo × Nota_Dados_Oficiais) + (Peso_Notícias × Sentimento_Notícias)
    - Sugestão inicial: Peso_Objetivo = 0,5 e Peso_Notícias = 0,5 (ajustável por configuração).
- Componentes
  - Nota_Dados_Oficiais (métricas objetivas, normalizadas por cargo/âmbito):
    - Presença/frequência em sessões.
    - Projetos apresentados/aprovados (ponderar qualidade/impacto quando houver dados).
    - Gastos de verba (transparência, eficiência, desvios).
    - Processos e condenações (ponderar estágio/gravidade, presunção de inocência observada conforme dados oficiais).
  - Sentimento_Notícias:
    - Análise de múltiplas fontes jornalísticas com NLP (classificação positiva/negativa/neutra + intensidade).
    - Ajuste por confiabilidade/viés da fonte e normalização por volume de cobertura.
  - Nota_Usuário:
    - Média ponderada das avaliações de usuários autenticados (1 voto por político a cada 30 dias por usuário), com técnicas de detecção de outliers e reputação do avaliador.

3. Funcionalidades do Sistema
- Autenticação & Segurança
  - Cadastro com CPF (1 conta por CPF) e verificação via API de validação (ex.: SERPRO).
  - Login com senha + 2FA opcional (e-mail/app autenticador/OTP).
  - Rate limiting e bloqueio de IPs para mitigar ataques automatizados/brute force.
- Página Inicial (Ranking)
  - Top 10 melhores e 10 piores por Poder:
    - Executivo: prefeitos, governadores, presidente.
    - Legislativo: vereadores, deputados, senadores.
    - Judiciário: ministros, desembargadores.
  - Filtros por região (estado, município), por cargo e ordenar por nota ou “tendência” (variação temporal).
- Página do Político
  - Perfil: foto, cargo, partido, mandato.
  - Nota geral + gráfico de evolução da nota.
  - Métricas objetivas (frequência, projetos, gastos, etc.).
  - Resumo da análise de notícias (quantidade positivas/negativas/neutras + fontes e intervalos).
  - Avaliação do usuário (nota e comentário) + exibição de comentários moderados.
- Filtros Avançados
  - Por cargo, estado/município, partido e temas (educação, saúde, segurança, etc.).

4. Fontes de Dados
- Oficiais
  - Portal da Transparência (execução orçamentária, gastos, etc.).
  - APIs da Câmara dos Deputados, Senado e Assembleias Legislativas (presença, proposições, votações).
  - TSE (dados de candidaturas, histórico eleitoral, bens declarados quando disponível).
  - Tribunais (processos, andamentos, decisões — respeitando limites legais e LGPD).
- Notícias
  - APIs como Google News API ou GDELT (quando política de uso permitir).
  - Web scraping (BeautifulSoup/Scrapy) apenas quando permitido pelos termos de uso e respeitando robots.txt.
  - Armazenamento e reprocessamento periódico para manter histórico e recalcular sentimentos.

5. Pipeline de Análise de Notícias (IA)
- Coleta: múltiplas fontes com espectros políticos diferentes.
- Processamento:
  - Deduplicação, extração de texto, identificação de entidades (políticos, cargos, partidos, lugares).
  - Classificação de sentimento (Hugging Face/transformers com BERTimbau, spaCy, ou NLTK conforme benchmark).
- Ponderação & Normalização:
  - Peso por confiabilidade/viés da fonte (tabela de pesos configurável + revisão editorial).
  - Normalização por volume de cobertura e tempo (evitar enviesamento por picos).
- Agregação:
  - Cálculo de Sentimento_Notícias por janela temporal (ex.: 7/30/90 dias) e por nível (municipal/estadual/federal).

6. Segurança, Moderação e Antimanipulação
- Contas de usuário
  - 1 conta por CPF validado; 2FA opcional; senhas com hash seguro (Argon2/bcrypt), política de complexidade.
  - Limite de 1 voto por político a cada 30 dias por usuário.
- Anti-bot & Integridade
  - Rate limiting por IP/usuário, CAPTCHA quando necessário, detecção de padrões suspeitos.
- Moderação de Conteúdo
  - IA para moderação de comentários (discurso de ódio, ataques pessoais, spam, fake news) + fila de revisão humana para casos limítrofes.
- Compliance & Auditoria
  - Adequação à LGPD (bases legais, consentimento, minimização de dados, direitos do titular, DPO).
  - Logs de auditoria para alterações de pesos, regras e dados agregados.

7. Arquitetura & Tecnologias
- Back-end
  - Django (Python) + Django REST Framework (APIs RESTful).
  - PostgreSQL (dados principais) e Redis (cache, rate limit, sessões).
  - Celery + broker (Redis) para tarefas assíncronas (coleta/ETL, NLP, reprocessamentos periódicos).
- Front-end
  - React + Vite (SPA) e TailwindCSS.
- IA & NLP
  - Python com transformers (BERTimbau), spaCy e/ou NLTK; pipelines de pré-processamento e inferência.
- Infra & DevOps
  - Docker e docker-compose (desenvolvimento e produção), variáveis de ambiente, secrets externos.
  - Observabilidade: logs estruturados, métricas e alertas.

8. Fluxo do Usuário
- Cadastro → Validação de CPF → Login (2FA opcional) → Página inicial com rankings.
- Pesquisa/filtros → Página do político.
- Avaliação (nota + comentário) → Moderação automática → Publicação sob regras.
- Retorno ao ranking e possibilidade de salvar filtros favoritos.

9. Extras Possíveis
- Comparador de políticos lado a lado.
- Modo “customizar ranking” (usuário ajusta pesos das métricas, com transparência do impacto).
- API pública para consulta a dados agregados (limites e chaves de acesso).

10. Roadmap (proposto, iterativo)
- Fase 0: Setup do projeto (Django/DRF, React/Vite, Docker, PostgreSQL/Redis, autenticação base).
- Fase 1: Modelo de dados de políticos, cargos, regiões; ingestão inicial de dados oficiais.
- Fase 2: Rankings básicos com Nota_Dados_Oficiais; página do político.
- Fase 3: Coleta de notícias + pipeline NLP + Sentimento_Notícias; composição Nota_IA.
- Fase 4: Avaliações de usuários, moderação, anti-abuso; composição Nota_Final.
- Fase 5: Filtros avançados, gráficos de tendência, comparador e API pública.
- Fase 6: Ajustes finos, auditoria/transparência, documentação e lançamento.

11. Transparência e Explicabilidade
- Página pública descrevendo metodologia, pesos, fontes e limitações.
- Para cada político: breakdown de notas (objetivo vs. notícias vs. usuário) + histórico de alterações de pesos sistêmicos.
- Exposição de amostras de fontes (links) e janelas temporais usadas no cálculo.


- Planejar os primeiros conectores de dados oficiais (prioridade: Câmara/Senado) e o MVP de ranking com dados objetivos.