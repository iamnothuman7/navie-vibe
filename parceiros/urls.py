from django.urls import path
from . import views

app_name = 'parceiros'

urlpatterns = [
    path('parceiros/solicitar/', views.solicitar_parceria, name='solicitar_parceria'),
    path('parceiros/doc/<slug:slug>/', views.ver_documento, name='ver_documento'),
]
