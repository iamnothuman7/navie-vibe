from django.db import models

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

class Hotel(models.Model): # Antigo 'Evento' adaptado para acomodacao/hotel principal
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    banner = models.ImageField(upload_to='hoteis/banners/', null=True, blank=True)
    
    # Relações
    local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name='hoteis')
    produtor = models.ForeignKey(Produtor, on_delete=models.SET_NULL, null=True, blank=True)
    
    status = models.CharField(max_length=50, default='ativo', choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')])
    destaque = models.BooleanField(default=False)
    
    data_inicio = models.DateField(null=True, blank=True) # Prazo de estadia/evento se houver
    horario_inicio = models.TimeField(null=True, blank=True)
    
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
    descricao = models.CharField(max_length=255, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"
