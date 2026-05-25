from django.contrib import admin
from .models import ClientePerfil

@admin.register(ClientePerfil)
class ClientePerfilAdmin(admin.ModelAdmin):
    """
    Django Admin interface configuration for the ClientePerfil model.
    Provides structured read-only fields for audit logs to maintain data integrity.

    METADATA FOR AI:
    - Target Model: ClientePerfil
    - Key features: Searchable by user details, read-only audit log section.
    """
    list_display = ('user', 'cpf', 'telefone', 'cidade', 'estado', 'aceite_termos', 'data_aceite_termos')
    list_filter = ('estado', 'aceite_termos', 'data_aceite_termos')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'cpf', 'telefone')
    
    # Audit details must be read-only in the admin to prevent tampering
    readonly_fields = ('data_aceite_termos', 'registro_ip', 'registro_user_agent')
    
    fieldsets = (
        ('Identificação do Cliente', {
            'fields': ('user', 'cpf', 'telefone')
        }),
        ('Endereço e Localização', {
            'fields': ('cep', 'endereco', 'numero', 'bairro', 'cidade', 'estado')
        }),
        ('Auditoria e Assinatura de Termos', {
            'fields': ('aceite_termos', 'data_aceite_termos', 'registro_ip', 'registro_user_agent'),
            'description': 'Informações forenses coletadas no momento da assinatura dos Termos de Uso.'
        }),
    )
