import os
import glob
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'navievibe.settings')
django.setup()

from hoteis.models import Quarto, QuartoImagem
from django.core.files import File

brain_dir = r'C:\Users\mateu\.gemini\antigravity\brain\17f010dd-1797-4f03-8d92-2926629161a6'

mappings = {
    'Suíte Casal Premium': 'suite_casal_*.png',
    'Quarto Simples': 'quarto_simples_*.png',
    'Master Suit': 'master_suit_*.png',
    'Chalé do Bosque': 'chale_*.png'
}

for nome_q, pattern in mappings.items():
    try:
        q = Quarto.objects.get(nome=nome_q)
    except Quarto.DoesNotExist:
        continue
        
    print(f'Limpando galerias do {nome_q}')
    QuartoImagem.objects.filter(quarto=q).delete()
    
    files = glob.glob(os.path.join(brain_dir, pattern))
    files.sort()
    
    for idx, f in enumerate(files):
        print(f'Adicionando imagem {f}')
        obj = QuartoImagem(quarto=q, ordem=idx)
        with open(f, 'rb') as fp:
            obj.url_imagem.save(os.path.basename(f), File(fp), save=True)

print('As galerias dos quartos foram estocadas com sucesso!')
