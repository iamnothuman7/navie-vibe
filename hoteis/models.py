from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid
import unicodedata
import re

class Produtor(models.Model):
    nome_publico = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nome_publico

class Local(models.Model):
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    
    def __str__(self):
        return f"{self.nome} - {self.cidade}/{self.estado}"

from core.models import Empresa

class Hotel(models.Model): # Representa a operação de Hospedagem de uma Empresa
    empresa = models.OneToOneField(
        Empresa, 
        on_delete=models.CASCADE, 
        related_name='perfil_hospedagem',
        null=True, blank=True,
        db_constraint=False,
        help_text="A entidade comercial dona desta hospedagem"
    )
    nome = models.CharField(max_length=255) # Pode ser diferente do Nome Fantasia se desejar
    descricao = models.TextField()
    banner = models.ImageField(upload_to='hoteis/banners/', null=True, blank=True)
    
    # Relações
    local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name='hoteis')
    produtor = models.ForeignKey(Produtor, on_delete=models.SET_NULL, null=True, blank=True)
    
    status = models.CharField(max_length=50, default='ativo', choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], db_index=True)
    destaque = models.BooleanField(default=False)
    
    data_inicio = models.DateField(null=True, blank=True) # Prazo de estadia/evento se houver
    horario_inicio = models.TimeField(null=True, blank=True)
    
    # Configurações & Branding do Site/Sistema
    cor_primaria = models.CharField(max_length=7, default='#f97316', help_text="Cor primária em formato Hexadecimal (ex: #f97316)")
    whatsapp = models.CharField(max_length=20, blank=True, null=True, help_text="WhatsApp de contato do hotel")
    hero_tipo = models.CharField(
        max_length=10, 
        default='imagem', 
        choices=[('imagem', 'Imagem'), ('video', 'Vídeo')],
        help_text="Tipo de mídia a ser exibida no cabeçalho/Hero do site"
    )
    hero_video = models.FileField(upload_to='hoteis/videos/', null=True, blank=True, help_text="Vídeo curto em loop (MP4 de até 8MB)")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="Coordenada geográfica de latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text="Coordenada geográfica de longitude")
    logo = models.ImageField(upload_to='hoteis/logos/', null=True, blank=True, help_text="Logo oficial da pousada")
    foto_fundo = models.ImageField(upload_to='hoteis/fundos/', null=True, blank=True, help_text="Imagem de fundo para o modo Glassmorphism")
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True, help_text="Slug da URL customizada (ex: pousadaramilostiangua)")


    
    def __str__(self):
        return self.nome

class HotelImagem(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='imagens')
    url_imagem = models.ImageField(upload_to='hoteis/galeria/')
    ordem = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordem']

class Quarto(models.Model): # Antigo 'Tipos de Ingresso'
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='quartos')
    nome = models.CharField(max_length=150) # Ex: Suite Master
    slug = models.SlugField(max_length=180, blank=True, help_text="URL amigável gerada automaticamente pelo nome")
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Novos campos para gestão avançada, SEO e IA
    video_url = models.CharField(max_length=500, blank=True, null=True, help_text="Link para vídeo MP4 ou embed")
    video_arquivo = models.FileField(upload_to='quartos/videos/', blank=True, null=True, help_text="Arquivo de vídeo local do tour")
    capacidade_pessoas = models.IntegerField(default=2, help_text="Capacidade de hóspedes")
    tags = models.CharField(max_length=255, blank=True, default="", help_text="Categorização (ex: Família, Romântico)")
    comodidades = models.CharField(max_length=255, blank=True, default="", help_text="Comodidades (ex: Ar Condicionado, Wi-Fi)")
    
    # Descontos progressivos
    tem_desconto_multidias = models.BooleanField(default=False)
    dias_minimos_desconto = models.IntegerField(default=3, help_text="Mínimo de dias para ativar desconto")
    percentual_desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Desconto em percentual (ex: 10.00 para 10%)")
    
    # Otimização SEO e Assistentes IA (ex: Google Gemini)
    seo_titulo = models.CharField(max_length=150, blank=True, null=True, help_text="Título customizado para buscadores/IA")
    seo_descricao = models.TextField(blank=True, null=True, help_text="Descrição customizada para buscadores/IA")
    
    class Meta:
        # Garante que o slug é único dentro de cada hotel (não globalmente)
        unique_together = [('hotel', 'slug')]
    
    @staticmethod
    def _normalizar_slug(texto):
        """Converte caracteres acentuados para ASCII antes de slugify."""
        nfkd = unicodedata.normalize('NFKD', texto)
        ascii_str = nfkd.encode('ascii', 'ignore').decode('ascii')
        return slugify(ascii_str)
    
    def _gerar_slug_unico(self):
        """Gera slug único por hotel, adicionando sufixo numérico se necessário."""
        base_slug = self._normalizar_slug(self.nome) or f'acomodacao-{self.id or 0}'
        candidato = base_slug
        num = 2
        while True:
            conflito = Quarto.objects.filter(hotel=self.hotel, slug=candidato)
            if self.pk:
                conflito = conflito.exclude(pk=self.pk)
            if not conflito.exists():
                return candidato
            candidato = f'{base_slug}-{num}'
            num += 1
    
    def save(self, *args, **kwargs):
        # Regera slug sempre que o nome mudar ou slug estiver vazio
        if not self.slug or (self.pk and Quarto.objects.filter(pk=self.pk).values_list('nome', flat=True).first() != self.nome):
            self.slug = self._gerar_slug_unico()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"

class QuartoImagem(models.Model):
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE, related_name='imagens')
    url_imagem = models.ImageField(upload_to='quartos/galeria/')
    ordem = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f"Img {self.ordem} - {self.quarto.nome}"

class UnidadeQuarto(models.Model):
    """Representa a sala física real de uma categoria de quarto, ex: Quarto 101, Chale 2"""
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE, related_name='unidades')
    identificador = models.CharField(max_length=50, help_text="Ex: 101, Chale 01, Deck Master")
    ativa = models.BooleanField(default=True, db_index=True)
    
    def __str__(self):
        return f"{self.identificador} ({self.quarto.nome})"

class Reserva(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmada', 'Confirmada'),
        ('hospedado', 'Hospedado'),
        ('concluido', 'Concluído'),
        ('cancelada', 'Cancelada'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reservas', db_constraint=False)
    unidade = models.ForeignKey(UnidadeQuarto, on_delete=models.PROTECT, related_name='reservas')
    data_checkin = models.DateField(db_index=True)
    data_checkout = models.DateField(db_index=True)
    
    # Valores financeiros
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    taxas = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', db_index=True)
    canal_venda = models.CharField(max_length=50, default='marketplace', help_text="marketplace ou walk-in")
    
    # Datas de execução reais de portaria
    checkin_realizado_em = models.DateTimeField(null=True, blank=True)
    checkout_realizado_em = models.DateTimeField(null=True, blank=True)
    
    # Ficha de Registro Nacional de Hóspedes (FNRH) histórica da reserva
    hospede_nome = models.CharField(max_length=255, blank=True, null=True)
    hospede_cpf = models.CharField(max_length=20, blank=True, null=True)
    hospede_email = models.EmailField(blank=True, null=True)
    hospede_telefone = models.CharField(max_length=20, blank=True, null=True)
    hospede_rg = models.CharField(max_length=50, blank=True, null=True)
    hospede_nacionalidade = models.CharField(max_length=100, blank=True, null=True)
    hospede_profissao = models.CharField(max_length=100, blank=True, null=True)
    hospede_endereco = models.TextField(blank=True, null=True)
    quantidade_hospedes = models.PositiveIntegerField(default=1)
    taxa_servico_plataforma = models.DecimalField('Taxa de Serviço Naviê', max_digits=10, decimal_places=2, default=0.00)
    taxa_gateway = models.DecimalField('Taxa Gateway Absorvida', max_digits=10, decimal_places=2, default=0.00)
    repasse_parceiro = models.DecimalField('Repasse Líquido ao Parceiro', max_digits=10, decimal_places=2, default=0.00)
    ganho_liquido_plataforma = models.DecimalField('Ganho Líquido Naviê', max_digits=10, decimal_places=2, default=0.00)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    @property
    def noites(self):
        if self.data_checkin and self.data_checkout:
            return (self.data_checkout - self.data_checkin).days
        return 1
        
    def __str__(self):
        return f"Reserva #{str(self.id)[:8].upper()} - {self.unidade.identificador}"

class BloqueioQuarto(models.Model):
    """Permite ao hotel bloquear datas por manutenção ou indisponibilidade"""
    unidade = models.ForeignKey(UnidadeQuarto, on_delete=models.CASCADE, related_name='bloqueios')
    data_inicio = models.DateField(db_index=True)
    data_fim = models.DateField(db_index=True)
    motivo = models.CharField(max_length=255, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Bloqueio {self.unidade.identificador} ({self.data_inicio} até {self.data_fim})"

class ParceiroUsuario(models.Model):
    ROLE_CHOICES = [
        ('proprietario', 'Proprietário'),
        ('gerente', 'Gerente'),
        ('portaria', 'Portaria / Recepção'),
        ('camareira', 'Camareira / Limpeza'),
        ('manutencao', 'Manutenção'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_parceiro', db_constraint=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='equipe', db_constraint=False)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='portaria')
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True, help_text="Formato: 000.000.000-00")
    ativo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()} ({self.hotel.nome})"


class Tarefa(models.Model):
    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('normal', 'Normal'),
        ('alta', 'Alta'),
    ]
    STATUS_CHOICES = [
        ('todo', 'A Fazer'),
        ('doing', 'Em Progresso'),
        ('done', 'Concluído'),
    ]
    
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='tarefas')
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='normal')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo', db_index=True)
    data_vencimento = models.DateField(blank=True, null=True, db_index=True)
    
    # Mapeamentos para Hospedagem:
    responsavel = models.ForeignKey(ParceiroUsuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='tarefas_atribuidas')
    unidade = models.ForeignKey(UnidadeQuarto, on_delete=models.SET_NULL, blank=True, null=True, related_name='tarefas')
    reserva = models.ForeignKey(Reserva, on_delete=models.SET_NULL, blank=True, null=True, related_name='tarefas')
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} - {self.get_status_display()}"
        
    @property
    def is_atrasada(self):
        from datetime import date
        if self.data_vencimento and self.data_vencimento < date.today() and self.status != 'done':
            return True
        return False


class HospedeReserva(models.Model):
    """FNRH individual de cada hóspede da reserva."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='hospedes')
    ordem = models.PositiveSmallIntegerField(default=1)  # 1 = titular, 2+ = acompanhantes
    
    # Dados pessoais (FNRH)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    rg = models.CharField(max_length=50, blank=True)
    nacionalidade = models.CharField(max_length=100, default='Brasileira')
    profissao = models.CharField(max_length=100, blank=True)
    endereco = models.TextField(blank=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordem']
        unique_together = ['reserva', 'ordem']


class VeiculoReserva(models.Model):
    """Veículo registrado para a reserva (controle de estacionamento)."""
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='veiculo')
    placa = models.CharField(max_length=10)
    modelo = models.CharField(max_length=100, blank=True)
    cor = models.CharField(max_length=50, blank=True)


