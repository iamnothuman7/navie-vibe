from django.db import models
from core.models import Empresa


class Cinema(models.Model):
    empresa = models.OneToOneField(Empresa, on_delete=models.CASCADE, related_name='perfil_cinema', db_constraint=False)
    possui_bonbonniere = models.BooleanField(default=True)
    descricao_cinema = models.TextField(blank=True)

    def __str__(self):
        return f"Cinema: {self.empresa.nome_fantasia}"


class Sala(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='salas')
    nome = models.CharField(max_length=50) # Ex: Sala 1, Sala VIP
    capacidade = models.PositiveIntegerField()
    formato_som = models.CharField(max_length=100, default='Dolby Digital 7.1')
    formato_imagem = models.CharField(max_length=100, default='4K Laser')
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} - {self.cinema.empresa.nome_fantasia}"


class Filme(models.Model):
    titulo = models.CharField(max_length=255)
    titulo_original = models.CharField(max_length=255, blank=True)
    duracao_minutos = models.PositiveIntegerField()
    classificacao_indicativa = models.CharField(max_length=20, default='Livre')
    genero = models.CharField(max_length=100)
    sinopse = models.TextField()
    poster = models.ImageField(upload_to='filmes/posters/')
    trailer_url = models.URLField(blank=True)
    em_cartaz = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo


class Sessao(models.Model):
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='sessoes')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='sessoes')
    horario = models.DateTimeField()
    preco_inteira = models.DecimalField(max_digits=10, decimal_places=2)
    preco_meia = models.DecimalField(max_digits=10, decimal_places=2)
    idioma = models.CharField(max_length=50, choices=[('dub', 'Dublado'), ('leg', 'Legendado')], default='dub')
    tecnologia = models.CharField(max_length=20, choices=[('2d', '2D'), ('3d', '3D')], default='2d')

    class Meta:
        verbose_name = 'Sessão'
        verbose_name_plural = 'Sessões'
        ordering = ['horario']

    def __str__(self):
        return f"{self.filme.titulo} - {self.horario.strftime('%d/%m %H:%M')}"
