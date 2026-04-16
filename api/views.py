from rest_framework import viewsets
from hoteis.models import Hotel
from .serializers import HotelSerializer

class HotelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint para listar os hotéis para futuros aplicativos mobiles.
    """
    queryset = Hotel.objects.filter(status='ativo').order_by('-destaque', 'id')
    serializer_class = HotelSerializer
