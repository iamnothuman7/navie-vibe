from django.shortcuts import render, get_object_or_404
from .models import Hotel

def home(request):
    destaque = Hotel.objects.filter(destaque=True, status='ativo').first()
    proximos = Hotel.objects.filter(status='ativo').order_by('id')[:6]
    
    context = {
        'destaque': destaque,
        'proximos': proximos,
    }
    return render(request, 'hoteis/home.html', context)

def detalhe(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    quartos = hotel.quartos.all()
    imagens = hotel.imagens.all()
    
    context = {
        'hotel': hotel,
        'quartos': quartos,
        'imagens': imagens,
    }
    return render(request, 'hoteis/detalhe.html', context)
