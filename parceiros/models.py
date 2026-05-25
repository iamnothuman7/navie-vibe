from django.db import models
from django.utils import timezone


class TipoEmpresa(models.TextChoices):
    HOTEL_POUSADA = 'hotel_pousada', 'Hotel / Pousada'
    CINEMA = 'cinema', 'Cinema'
    CASA_SHOWS = 'casa_shows', 'Casa de Shows'
    PRODUTOR_EVENTOS = 'produtor_eventos', 'Produtor de Eventos'
    RESTAURANTE = 'restaurante', 'Restaurante / Gastronomia'
    PARQUE_TURISMO = 'parque_turismo', 'Parque / Turismo'
    OUTRO = 'outro', 'Outro'


class StatusSolicitacao(models.TextChoices):
    PENDENTE = 'pendente', 'Pendente'
    EM_CONTATO = 'em_contato', 'Em Contato'
    APROVADO = 'aprovado', 'Aprovado'
    RECUSADO = 'recusado', 'Recusado'
    AGUARDANDO_DOCUMENTACAO = 'aguardando_doc', 'Aguardando Documentação'


class SolicitacaoEmpresa(models.Model):
    """
    Armazena cada solicitação de parceria enviada pelo formulário.
    Dados completamente isolados — nunca misturar com dados de hoteis/.
    """

    # ─── Identificação da Empresa ─────────────────────────────────────────────
    razao_social = models.CharField('Razão Social', max_length=200)
    nome_fantasia = models.CharField('Nome Fantasia', max_length=200)
    cnpj = models.CharField('CNPJ', max_length=18)  # XX.XXX.XXX/XXXX-XX
    tipo_empresa = models.CharField(
        'Tipo de Negócio',
        max_length=30,
        choices=TipoEmpresa.choices,
    )
    site = models.URLField('Site Institucional', blank=True)
    instagram = models.CharField('Instagram / Redes Sociais', max_length=200, blank=True)

    # ─── Localização ──────────────────────────────────────────────────────────
    cep = models.CharField('CEP', max_length=9)
    endereco = models.CharField('Endereço (Rua/Av)', max_length=300)
    numero = models.CharField('Número', max_length=20)
    bairro = models.CharField('Bairro', max_length=100, blank=True)
    cidade = models.CharField('Cidade', max_length=100)
    estado = models.CharField('Estado (UF)', max_length=2)

    # ─── Responsável pelo Cadastro ────────────────────────────────────────────
    responsavel_nome = models.CharField('Nome do Responsável', max_length=150)
    responsavel_cargo = models.CharField('Cargo / Função', max_length=100)
    responsavel_email = models.EmailField('E-mail Corporativo')
    responsavel_telefone = models.CharField('Telefone / WhatsApp', max_length=20)

    # ─── Sobre o Negócio ──────────────────────────────────────────────────────
    descricao_negocio = models.TextField(
        'Descrição do Negócio',
        help_text='O que a empresa oferece, capacidade, diferenciais...'
    )
    capacidade = models.CharField(
        'Capacidade / Tamanho',
        max_length=200,
        blank=True,
        help_text='Ex: 20 quartos, 300 lugares, etc.'
    )
    como_soube = models.CharField(
        'Como ficou sabendo do Naviê?',
        max_length=200,
        blank=True,
    )

    # ─── Aceites Legais ───────────────────────────────────────────────────────
    aceite_termos = models.BooleanField('Aceita Termos de Parceria', default=False)
    aceite_privacidade = models.BooleanField('Aceita Política de Privacidade', default=False)
    autoriza_contato = models.BooleanField('Autoriza contato da equipe Naviê', default=False)

    # ─── Controle Interno ─────────────────────────────────────────────────────
    status = models.CharField(
        'Status',
        max_length=20,
        choices=StatusSolicitacao.choices,
        default=StatusSolicitacao.PENDENTE,
    )
    notas_internas = models.TextField(
        'Notas Internas',
        blank=True,
        help_text='Observações da equipe Naviê (não visível ao solicitante)'
    )
    data_solicitacao = models.DateTimeField('Data da Solicitação', default=timezone.now)
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)
    atendido_por = models.CharField(
        'Atendido por',
        max_length=100,
        blank=True,
        help_text='Nome do membro da equipe Naviê responsável'
    )

    class Meta:
        app_label = 'parceiros'
        verbose_name = 'Solicitação de Empresa'
        verbose_name_plural = 'Solicitações de Empresas'
        ordering = ['-data_solicitacao']
        # Garante isolamento de dados — tabela própria do app
        db_table = 'parceiros_solicitacao_empresa'

    def __str__(self):
        return f'{self.nome_fantasia} ({self.get_tipo_empresa_display()}) — {self.get_status_display()}'

    @property
    def aceites_completos(self):
        return self.aceite_termos and self.aceite_privacidade and self.autoriza_contato


class Documento(models.Model):
    """
    Documentos editáveis pelo admin: Termos de Parceria, Política de Privacidade, etc.
    """
    SLUG_CHOICES = [
        ('termos-parceria', 'Termos de Parceria'),
        ('politica-privacidade', 'Política de Privacidade'),
    ]

    slug = models.SlugField('Identificador', max_length=60, unique=True, choices=SLUG_CHOICES)
    titulo = models.CharField('Título', max_length=200)
    conteudo = models.TextField(
        'Conteúdo (HTML)',
        help_text='Pode usar HTML básico: &lt;h2&gt;, &lt;p&gt;, &lt;ul&gt;, &lt;strong&gt;, etc.'
    )
    atualizado_em = models.DateTimeField('Última Atualização', auto_now=True)

    class Meta:
        app_label = 'parceiros'
        verbose_name = 'Documento Legal'
        verbose_name_plural = 'Documentos Legais'
        db_table = 'parceiros_documento'

    def __str__(self):
        return self.titulo
