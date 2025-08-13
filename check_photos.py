from core.models import Politico

print('Políticos com foto:')
for p in Politico.objects.all():
    print(f'{p.nome}: foto={bool(p.foto)}, foto_url={p.foto_url}')