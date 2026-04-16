import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'navievibe.settings')
django.setup()

from hoteis.models import Local, Hotel, Quarto

# Clear existing
Hotel.objects.all().delete()
Local.objects.all().delete()

# Create Locals
l1 = Local.objects.create(nome="Serra Premium", endereco="Serra da Ibiapaba, Rural", cidade="Tianguá", estado="CE")
l2 = Local.objects.create(nome="Alto Viçosa", endereco="Rua Matriz, 123", cidade="Viçosa do Ceará", estado="CE")
l3 = Local.objects.create(nome="Encanto Ubajara", endereco="Estrada do Parque, S/N", cidade="Ubajara", estado="CE")

# Import images paths
img1_path = r"C:\Users\mateu\.gemini\antigravity\brain\17f010dd-1797-4f03-8d92-2926629161a6\pousada_serra_banner_1776308339568.png"
img2_path = r"C:\Users\mateu\.gemini\antigravity\brain\17f010dd-1797-4f03-8d92-2926629161a6\hotel_luxo_banner_1776308353879.png"
img3_path = r"C:\Users\mateu\.gemini\antigravity\brain\17f010dd-1797-4f03-8d92-2926629161a6\chales_madeira_banner_1776308369021.png"

h1 = Hotel(nome="Pousada da Serra", descricao="Uma pousada maravilhosa na serra da Ibiapaba com uma natureza rica e luzes quentes para relaxar.", local=l1, status="ativo", destaque=True, data_inicio="2026-12-01", horario_inicio="14:00")
if os.path.exists(img1_path):
    with open(img1_path, 'rb') as f:
        h1.banner.save('pousada_serra.png', File(f), save=True)
else:
    h1.save()

h2 = Hotel(nome="Hotel Luxo Ibiapaba", descricao="Conforto moderno com vista infinita para o vale verde impecável. Um respiro profundo e total paz.", local=l2, status="ativo", destaque=False)
if os.path.exists(img2_path):
    with open(img2_path, 'rb') as f:
        h2.banner.save('hotel_luxo.png', File(f), save=True)
else:
    h2.save()

h3 = Hotel(nome="Chalés Maciço Suíço", descricao="Chalés aconchegantes de madeira pura abraçados por uma floresta inteira na Ibiapaba.", local=l3, status="ativo", destaque=False)
if os.path.exists(img3_path):
    with open(img3_path, 'rb') as f:
        h3.banner.save('chales.png', File(f), save=True)
else:
    h3.save()

# Quartos
Quarto.objects.create(hotel=h1, nome="Suíte Casal Premium", descricao="Cama King, Hidromassagem, Lareira", preco=550.00)
Quarto.objects.create(hotel=h1, nome="Quarto Simples", descricao="Cama Queen, Banheiro privado", preco=200.00)

Quarto.objects.create(hotel=h2, nome="Master Suit", descricao="Vista panorâmica do vale, sacada, café incluso na cama", preco=800.00)
Quarto.objects.create(hotel=h3, nome="Chalé do Bosque", descricao="Todo equipado, lareira externa privativa", preco=400.00)

print("Seed executed successfully.")
