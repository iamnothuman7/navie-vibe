from django.urls import path
from . import views

app_name = 'hoteis'

urlpatterns = [
    path('', views.home, name='home'),
    path('hotel/<int:hotel_id>/', views.detalhe, name='detalhe'),
    path('api/hotel/<int:hotel_id>/check_disponibilidade/', views.api_check_disponibilidade, name='check_disponibilidade'),
    path('api/hotel/<int:hotel_id>/datas_ocupadas/', views.api_datas_ocupadas, name='datas_ocupadas'),
    path('hotelaria/', views.hotelaria, name='hotelaria'),
    
    # Gestão Hoteleira (Naviê Hospedagens)
    path('hospedagens/auth/', views.partner_auth, name='partner_login'),
    path('hospedagens/logout/', views.partner_logout, name='partner_logout'),
    path('hospedagens/painel/', views.partner_dashboard, name='partner_dashboard'),
    path('hospedagens/ia_chat/', views.ia_enviar_chat, name='ia_enviar_chat'),
    path('hospedagens/atividades/criar/', views.partner_criar_tarefa, name='partner_criar_tarefa'),
    path('hospedagens/atividades/editar/<int:tarefa_id>/', views.partner_editar_tarefa, name='partner_editar_tarefa'),
    path('hospedagens/atividades/deletar/<int:tarefa_id>/', views.partner_deletar_tarefa, name='partner_deletar_tarefa'),
    path('hospedagens/atividades/mudar-status/<int:tarefa_id>/', views.partner_mudar_status_tarefa, name='partner_mudar_status_tarefa'),
    path('hospedagens/configuracoes/salvar/', views.partner_salvar_configuracoes, name='partner_salvar_configuracoes'),
    
    # Gestão de Quartos (Reativa via HTMX)
    path('hospedagens/quartos/formulario/', views.partner_quarto_formulario, name='partner_quarto_formulario'),
    path('hospedagens/quartos/formulario/<int:quarto_id>/', views.partner_quarto_formulario, name='partner_quarto_formulario'),
    path('hospedagens/quartos/lista/', views.partner_quarto_lista, name='partner_quarto_lista'),
    path('hospedagens/quartos/salvar/', views.partner_quarto_salvar, name='partner_quarto_salvar'),
    path('hospedagens/quartos/deletar/<int:quarto_id>/', views.partner_quarto_deletar, name='partner_quarto_deletar'),
    path('hospedagens/quartos/imagem/deletar/<int:imagem_id>/', views.partner_quarto_deletar_imagem, name='partner_quarto_deletar_imagem'),
    
    path('<slug:slug>/', views.vanity_url, name='vanity_url'),
]


