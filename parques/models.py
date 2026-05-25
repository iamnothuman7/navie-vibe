from django.db import models
from core.models import Empresa
from hoteis.models import Hotel # Importamos Hotel do app hoteis


class Parque(models.Model):
    empresa = models.OneToOneField(Empresa, on_delete=models.CASCADE, related_name='perfil_parque', db_constraint=False)
    descricao_parque = models.TextField()
    
    # O Parque pode possuir uma ou mais estruturas de hospedagem vinculadas
    # Isso permite que ele use as ferramentas de 'Hoteis' (quartos, reservas)
    hospedagens_vinculadas = models.ManyToManyField(Hotel, blank=True, related_name='parques_donos', db_constraint=False)
    
    # Horário de Funcionamento Geral
    horario_abertura = models.TimeField(null=True, blank=True)
    horario_fechamento = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"Parque: {self.empresa.nome_fantasia}"


class Atracao(models.Model):
    parque = models.ForeignKey(Parque, on_delete=models.CASCADE, related_name='atracoes')
    nome = models.CharField(max_length=255) # Ex: Trilha do Mirante, Tirolesa 500m
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='parques/atracoes/', null=True, blank=True)
    
    # Preço se for cobrado à parte (pode ser gratuito se incluso na entrada)
    preco_adicional = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Controle de capacidade se necessário (ex: trilha guiada com limite de pessoas)
    tem_capacidade_limite = models.BooleanField(default=False)
    capacidade_maxima = models.PositiveIntegerField(null=True, blank=True)
    
    ativa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Atração'
        verbose_name_plural = 'Atrações'

    def __str__(self):
        return f"{self.nome} - {self.parque.empresa.nome_fantasia}"


class IngressoParque(models.Model):
    """Day Use ou Entrada Geral do Parque"""
    parque = models.ForeignKey(Parque, on_delete=models.CASCADE, related_name='ingressos')
    nome = models.CharField(max_length=100) # Ex: Day Use Adulto, Entrada Meia
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    validade_dias = models.PositiveIntegerField(default=1, help_text="Validade em dias após a compra")

    def __str__(self):
        return f"{self.nome} - {self.parque.empresa.nome_fantasia}"
