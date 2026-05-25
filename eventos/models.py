from django.db import models
from core.models import Empresa


class Produtora(models.Model):
    empresa = models.OneToOneField(Empresa, on_delete=models.CASCADE, related_name='perfil_produtora', db_constraint=False)
    especialidade = models.CharField(max_length=100, blank=True) # Ex: Shows de Rock, Eventos Infantis

    def __str__(self):
        return f"Produtora: {self.empresa.nome_fantasia}"


class Evento(models.Model):
    produtora = models.ForeignKey(Produtora, on_delete=models.CASCADE, related_name='eventos')
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    banner = models.ImageField(upload_to='eventos/banners/')
    data_evento = models.DateTimeField()
    local_nome = models.CharField(max_length=255) # Ex: Arena Ibiapaba
    
    status = models.CharField(max_length=20, choices=[
        ('planejado', 'Planejado'),
        ('vendas_abertas', 'Vendas Abertas'),
        ('esgotado', 'Esgotado'),
        ('cancelado', 'Cancelado'),
        ('encerrado', 'Encerrado'),
    ], default='planejado')

    class Meta:
        ordering = ['data_evento']

    def __str__(self):
        return self.nome


class Lote(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='lotes')
    numero_lote = models.PositiveIntegerField()
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    ativo = models.BooleanField(default=False)

    def __str__(self):
        return f"Lote {self.numero_lote} - {self.evento.nome}"


class TipoIngresso(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='tipos_ingresso')
    nome = models.CharField(max_length=100) # Ex: VIP, Pista, Frontstage
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_disponivel = models.PositiveIntegerField()
    quantidade_vendida = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nome} - {self.lote.evento.nome}"
