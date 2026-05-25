from django.urls import path
from . import views

# Routing namespace for the 'clientes' app.
# Allows standard reverse mapping like {% url 'clientes:painel' %}
app_name = 'clientes'

urlpatterns = [
    # ─── Page Render Views ───────────────────────────────────────────────────
    path('login/', views.login_cadastro_view, name='login_cadastro'),
    path('painel/', views.painel_view, name='painel'),
    
    # ─── AJAX API endpoints (Single Page authentication flow) ───────────────
    path('api/login/', views.api_login, name='api_login'),
    path('api/registrar/', views.api_registrar, name='api_registrar'),
    
    # ─── Session Destroy View ────────────────────────────────────────────────
    path('logout/', views.logout_view, name='logout'),
]
