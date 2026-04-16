from rest_framework import serializers
from hoteis.models import Hotel, Local, Quarto, HotelImagem

class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = '__all__'

class QuartoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarto
        fields = ['id', 'nome', 'descricao', 'preco']

class HotelImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImagem
        fields = ['url_imagem', 'ordem']

class HotelSerializer(serializers.ModelSerializer):
    local = LocalSerializer(read_only=True)
    quartos = QuartoSerializer(many=True, read_only=True)
    imagens = HotelImagemSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'nome', 'descricao', 'banner', 'status', 'destaque', 'data_inicio', 'horario_inicio', 'local', 'quartos', 'imagens']
