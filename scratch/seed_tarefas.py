import os
import sys
import django
from datetime import date, timedelta

# Adiciona o diretório raiz do projeto ao PATH do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define as configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'navievibe.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Empresa
from hoteis.models import Local, Hotel, Quarto, UnidadeQuarto, ParceiroUsuario, Reserva, Tarefa

print("Iniciando semeadura de dados hoteleiros completos para a Pousada Ramilos...")

# 1. Obter Hotel Ramilos
try:
    hotel = Hotel.objects.get(nome="Pousada Ramilos Tianguá")
    print(f"Hotel '{hotel.nome}' localizado com sucesso.")
except Hotel.DoesNotExist:
    print("ERRO: Execute seed_ramilos.py primeiro para criar o hotel e a empresa.")
    sys.exit(1)

# 2. Criar Categorias de Quartos (Quarto) no banco 'hospedagem'
q1, created_q1 = Quarto.objects.get_or_create(
    hotel=hotel,
    nome="Suíte Master Casal",
    defaults={
        'descricao': "Suíte luxo com cama King Size, varanda com vista para a serra, banheira de hidromassagem e frigobar completo.",
        'preco': 250.00
    }
)
q2, created_q2 = Quarto.objects.get_or_create(
    hotel=hotel,
    nome="Chalé Familiar Serra",
    defaults={
        'descricao': "Chalé rústico aconchegante de dois quartos, lareira ecológica, cozinha compacta e deck externo privativo.",
        'preco': 380.00
    }
)
q3, created_q3 = Quarto.objects.get_or_create(
    hotel=hotel,
    nome="Suíte Standard Single",
    defaults={
        'descricao': "Acomodação prática e confortável com cama de solteiro, ar-condicionado, Wi-Fi ultra-rápido e mesa de trabalho.",
        'preco': 150.00
    }
)
print("Categorias de quartos criadas/verificadas.")

# 3. Criar Unidades Físicas (UnidadeQuarto)
u101, _ = UnidadeQuarto.objects.get_or_create(quarto=q1, identificador="Suíte 101", defaults={'ativa': True})
u102, _ = UnidadeQuarto.objects.get_or_create(quarto=q1, identificador="Suíte 102", defaults={'ativa': True})

uchale1, _ = UnidadeQuarto.objects.get_or_create(quarto=q2, identificador="Chalé 01", defaults={'ativa': True})
uchale2, _ = UnidadeQuarto.objects.get_or_create(quarto=q2, identificador="Chalé 02", defaults={'ativa': True})

u103, _ = UnidadeQuarto.objects.get_or_create(quarto=q3, identificador="Suíte 103", defaults={'ativa': True})
u104, _ = UnidadeQuarto.objects.get_or_create(quarto=q3, identificador="Suíte 104", defaults={'ativa': True})
print("Unidades físicas dos quartos criadas/verificadas.")

# 4. Criar Colaboradores / Equipe (ParceiroUsuario)
colaboradores = [
    {
        'username': 'mariacamareira',
        'first_name': 'Maria',
        'last_name': 'Camareira',
        'email': 'maria.camareira@ramilos.com',
        'role': 'camareira',
        'cpf': '222.333.444-55'
    },
    {
        'username': 'carlosmanutencao',
        'first_name': 'Carlos',
        'last_name': 'Manutenção',
        'email': 'carlos.manutencao@ramilos.com',
        'role': 'manutencao',
        'cpf': '333.444.555-66'
    },
    {
        'username': 'robertoportaria',
        'first_name': 'Roberto',
        'last_name': 'Portaria',
        'email': 'roberto.portaria@ramilos.com',
        'role': 'portaria',
        'cpf': '444.555.666-77'
    }
]

print("Criando usuários de equipe...")
for c in colaboradores:
    if not User.objects.filter(username=c['username']).exists():
        u = User.objects.create_user(
            username=c['username'],
            email=c['email'],
            password='senha123',
            first_name=c['first_name'],
            last_name=c['last_name']
        )
    else:
        u = User.objects.get(username=c['username'])
        
    ParceiroUsuario.objects.get_or_create(
        user=u,
        defaults={
            'hotel': hotel,
            'role': c['role'],
            'cpf': c['cpf'],
            'ativo': True
        }
    )
print("Equipe operacional cadastrada/verificada.")

# 5. Criar Reservas de Exemplo (Reserva)
guest_user, _ = User.objects.get_or_create(
    username="hospedeteste",
    defaults={
        'email': 'hospede@gmail.com',
        'first_name': 'João',
        'last_name': 'Silva'
    }
)

Reserva.objects.get_or_create(
    unidade=u101,
    data_checkin=date.today() - timedelta(days=2),
    data_checkout=date.today() + timedelta(days=2),
    defaults={
        'usuario': guest_user,
        'valor_total': 1000.00,
        'status': 'confirmada'
    }
)

Reserva.objects.get_or_create(
    unidade=uchale2,
    data_checkin=date.today() - timedelta(days=1),
    data_checkout=date.today() + timedelta(days=3),
    defaults={
        'usuario': guest_user,
        'valor_total': 1520.00,
        'status': 'confirmada'
    }
)
print("Reservas de exemplo inseridas.")

# Obter perfis sem JOINs cross-database:
u_maria = User.objects.get(username='mariacamareira')
maria = ParceiroUsuario.objects.get(user_id=u_maria.id)

u_carlos = User.objects.get(username='carlosmanutencao')
carlos = ParceiroUsuario.objects.get(user_id=u_carlos.id)


# Limpar tarefas antigas para repopular limpo
Tarefa.objects.filter(hotel=hotel).delete()

tarefas_seed = [
    {
        'titulo': 'Limpeza pré-check-in',
        'descricao': 'Preparar quarto com enxoval completo de luxo e aromatização serrana.',
        'prioridade': 'normal',
        'status': 'todo',
        'data_vencimento': date.today(),
        'responsavel': maria,
        'unidade': u101
    },
    {
        'titulo': 'Revisar vazamento do chuveiro',
        'descricao': 'Chuveiro elétrico pingando mesmo fechado. Verificar vedações.',
        'prioridade': 'alta',
        'status': 'doing',
        'data_vencimento': date.today(),
        'responsavel': carlos,
        'unidade': u103
    },
    {
        'titulo': 'Higienização pós check-out',
        'descricao': 'Limpeza pesada completa e troca de roupa de cama.',
        'prioridade': 'normal',
        'status': 'done',
        'data_vencimento': date.today() - timedelta(days=1),
        'responsavel': maria,
        'unidade': uchale2
    },
    {
        'titulo': 'Instalar novo roteador Wi-Fi',
        'descricao': 'Trocar roteador antigo por modelo Wi-Fi 6 Mesh para cobrir o deck externo.',
        'prioridade': 'normal',
        'status': 'todo',
        'data_vencimento': date.today() + timedelta(days=1),
        'responsavel': carlos,
        'unidade': uchale1
    },
    {
        'titulo': 'Vistoria e reposição do frigobar',
        'descricao': 'Repor águas, refrigerantes, cervejas artesanais e chocolates serranos.',
        'prioridade': 'baixa',
        'status': 'todo',
        'data_vencimento': date.today(),
        'responsavel': maria,
        'unidade': u102
    },
    {
        'titulo': 'Reposição de lenha para lareira',
        'descricao': 'Abastecer o estoque de lenha e acendedores ecológicos do chalé.',
        'prioridade': 'normal',
        'status': 'doing',
        'data_vencimento': date.today(),
        'responsavel': maria,
        'unidade': u104
    }
]

for t in tarefas_seed:
    Tarefa.objects.create(
        hotel=hotel,
        titulo=t['titulo'],
        descricao=t['descricao'],
        prioridade=t['prioridade'],
        status=t['status'],
        data_vencimento=t['data_vencimento'],
        responsavel=t['responsavel'],
        unidade=t['unidade']
    )

print("Tarefas reais semeadas com sucesso no pilar operacional B2B.")
print("\nSemeadura hoteleira completa concluída com absoluto sucesso!")
