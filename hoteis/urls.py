from django.urls import path
from . import views

app_name = 'hoteis'

urlpatterns = [
    path('', views.home, name='home'),
    path('hotel/<int:hotel_id>/', views.detalhe, name='detalhe'),
]
