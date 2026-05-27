from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from core.models import Empresa
from hoteis.models import Local, Hotel, Quarto, UnidadeQuarto, ParceiroUsuario, Reserva
from hoteis.views import partner_quarto_salvar
from django.contrib.messages.storage.base import BaseStorage
import datetime

class MockStorage(BaseStorage):
    def _get(self):
        return [], True
    def _store(self, messages, response, *args, **kwargs):
        return []

class PartnerQuartoSaveTestCase(TestCase):
    databases = '__all__'

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='partner_user', password='password123')
        self.empresa = Empresa.objects.create(
            nome_fantasia='Test Empresa',
            razao_social='Test Empresa LTDA',
            cnpj='12.345.678/0001-90',
            categoria='hospedagem',
            endereco='Av. Central, 100',
            cidade='Tianguá',
            estado='CE',
            cep='62320-000',
            email_contato='contato@test.com',
            telefone_contato='88999999999'
        )
        self.local = Local.objects.create(nome='Test Local', endereco='Av. Central, 100', cidade='Tianguá', estado='CE')
        self.hotel = Hotel.objects.create(
            empresa=self.empresa,
            nome='Pousada Ramilos',
            descricao='Pousada Teste',
            local=self.local,
            slug='pousadaramilos'
        )
        self.parceiro = ParceiroUsuario.objects.create(
            user=self.user,
            hotel=self.hotel,
            role='proprietario',
            ativo=True
        )

    def test_save_new_quarto_with_units(self):
        # Prepare POST data
        data = {
            'nome': 'Suíte Premium',
            'descricao': 'Descrição da suíte premium',
            'preco': '350.00',
            'capacidade_pessoas': '3',
            'tags': 'Casal, Serra',
            'comodidades': 'Ar Condicionado, Wi-Fi',
            'unidades_ids': ['new', 'new'],
            'unidades_identificadores': ['101', '102'],
        }
        
        request = self.factory.post('/hospedagens/quartos/formulario/salvar/', data)
        request.user = self.user
        
        # Enable messages framework in request using MockStorage
        setattr(request, '_messages', MockStorage(request))
        
        response = partner_quarto_salvar(request)
        self.assertEqual(response.status_code, 200)
        
        # Verify Quarto was created
        quarto = Quarto.objects.get(nome='Suíte Premium', hotel=self.hotel)
        self.assertEqual(quarto.preco, 350.00)
        self.assertEqual(quarto.capacidade_pessoas, 3)
        
        # Verify UnidadeQuarto instances were created
        units = list(quarto.unidades.filter(ativa=True).order_by('identificador'))
        self.assertEqual(len(units), 2)
        self.assertEqual(units[0].identificador, '101')
        self.assertEqual(units[1].identificador, '102')

    def test_edit_existing_quarto_units(self):
        # First, create a quarto with some units
        quarto = Quarto.objects.create(
            hotel=self.hotel,
            nome='Suíte Master',
            preco=400.00,
            capacidade_pessoas=2
        )
        u1 = UnidadeQuarto.objects.create(quarto=quarto, identificador='201', ativa=True)
        u2 = UnidadeQuarto.objects.create(quarto=quarto, identificador='202', ativa=True)
        
        # Now edit: update 201 to 201-A, keep 202, add new unit 203
        data = {
            'quarto_id': str(quarto.id),
            'nome': 'Suíte Master Modificada',
            'descricao': 'Nova desc',
            'preco': '450.00',
            'capacidade_pessoas': '2',
            'unidades_ids': [str(u1.id), str(u2.id), 'new'],
            'unidades_identificadores': ['201-A', '202', '203'],
        }
        
        request = self.factory.post('/hospedagens/quartos/formulario/salvar/', data)
        request.user = self.user
        setattr(request, '_messages', MockStorage(request))
        
        response = partner_quarto_salvar(request)
        self.assertEqual(response.status_code, 200)
        
        # Verify Quarto updated
        quarto.refresh_from_db()
        self.assertEqual(quarto.nome, 'Suíte Master Modificada')
        self.assertEqual(quarto.preco, 450.00)
        
        # Verify units updated and new added
        units = list(quarto.unidades.filter(ativa=True).order_by('identificador'))
        self.assertEqual(len(units), 3)
        self.assertEqual(units[0].identificador, '201-A')
        self.assertEqual(units[1].identificador, '202')
        self.assertEqual(units[2].identificador, '203')
        
        # Verify that u1 was updated (not recreated)
        u1.refresh_from_db()
        self.assertEqual(u1.identificador, '201-A')

    def test_delete_existing_quarto_unit(self):
        # Create a quarto with some units
        quarto = Quarto.objects.create(
            hotel=self.hotel,
            nome='Chalé Luxo',
            preco=500.00,
            capacidade_pessoas=4
        )
        u1 = UnidadeQuarto.objects.create(quarto=quarto, identificador='Ch-01', ativa=True)
        u2 = UnidadeQuarto.objects.create(quarto=quarto, identificador='Ch-02', ativa=True)
        
        # Edit and submit only Ch-01 (effectively removing Ch-02)
        data = {
            'quarto_id': str(quarto.id),
            'nome': 'Chalé Luxo',
            'descricao': 'Desc',
            'preco': '500.00',
            'capacidade_pessoas': '4',
            'unidades_ids': [str(u1.id)],
            'unidades_identificadores': ['Ch-01'],
        }
        
        request = self.factory.post('/hospedagens/quartos/formulario/salvar/', data)
        request.user = self.user
        setattr(request, '_messages', MockStorage(request))
        
        response = partner_quarto_salvar(request)
        self.assertEqual(response.status_code, 200)
        
        # Verify Ch-02 deleted
        active_units = list(quarto.unidades.filter(ativa=True))
        self.assertEqual(len(active_units), 1)
        self.assertEqual(active_units[0].identificador, 'Ch-01')
        
        # Verify Ch-02 is physically deleted
        self.assertFalse(UnidadeQuarto.objects.filter(id=u2.id).exists())

    def test_delete_existing_quarto_unit_with_booking_deactivates(self):
        # Create a quarto with some units
        quarto = Quarto.objects.create(
            hotel=self.hotel,
            nome='Chalé Booking',
            preco=500.00,
            capacidade_pessoas=4
        )
        u1 = UnidadeQuarto.objects.create(quarto=quarto, identificador='Ch-01', ativa=True)
        u2 = UnidadeQuarto.objects.create(quarto=quarto, identificador='Ch-02', ativa=True)
        
        # Create booking pointing to u2
        Reserva.objects.create(
            unidade=u2,
            data_checkin=datetime.date.today(),
            data_checkout=datetime.date.today() + datetime.timedelta(days=2),
            valor_total=1000.00,
            status='confirmada'
        )
        
        # Edit and submit only Ch-01 (effectively removing Ch-02, which is linked to a booking)
        data = {
            'quarto_id': str(quarto.id),
            'nome': 'Chalé Booking',
            'descricao': 'Desc',
            'preco': '500.00',
            'capacidade_pessoas': '4',
            'unidades_ids': [str(u1.id)],
            'unidades_identificadores': ['Ch-01'],
        }
        
        request = self.factory.post('/hospedagens/quartos/formulario/salvar/', data)
        request.user = self.user
        setattr(request, '_messages', MockStorage(request))
        
        response = partner_quarto_salvar(request)
        self.assertEqual(response.status_code, 200)
        
        # Verify Ch-01 remains active
        active_units = list(quarto.unidades.filter(ativa=True))
        self.assertEqual(len(active_units), 1)
        self.assertEqual(active_units[0].identificador, 'Ch-01')
        
        # Verify Ch-02 is deactivated (ativa=False) but still exists in database due to foreign key
        u2.refresh_from_db()
        self.assertFalse(u2.ativa)
        self.assertTrue(UnidadeQuarto.objects.filter(id=u2.id).exists())
