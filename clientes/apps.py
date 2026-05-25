from django.apps import AppConfig

class ClientesConfig(AppConfig):
    """
    Django configuration class for the 'clientes' (Clients) application.
    
    PURPOSE:
    This app manages all everyday customer profiles, authentication, 
    onboarding legal agreement audits (Terms of Use/Privacy Policy signing), 
    and the central client unified dashboard (reservations, movie, and show tickets).

    INTEGRATION & RELATIONSHIPS:
    - Extends Django's native auth.User model using a OneToOne profile (ClientePerfil).
    - Acts as a customer registry for bookings (hoteis.Reserva) and ticketing across all platform verticals.
    
    METADATA FOR AI:
    - Name: clientes
    - Label: clientes
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clientes'
    verbose_name = 'Portal de Clientes'
