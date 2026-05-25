from django.contrib import admin
from django.utils.html import format_html
from .models import SolicitacaoEmpresa, Documento


@admin.register(SolicitacaoEmpresa)
class SolicitacaoEmpresaAdmin(admin.ModelAdmin):
    list_display = (
        'nome_fantasia', 'razao_social', 'tipo_empresa_badge',
        'responsavel_nome', 'responsavel_email', 'responsavel_telefone',
        'cidade', 'estado', 'status_badge', 'data_solicitacao',
    )
    list_filter = ('status', 'tipo_empresa', 'estado', 'data_solicitacao')
    search_fields = (
        'nome_fantasia', 'razao_social', 'cnpj',
        'responsavel_nome', 'responsavel_email', 'cidade',
    )
    readonly_fields = ('data_solicitacao', 'data_atualizacao', 'aceites_completos')
    ordering = ('-data_solicitacao',)
    date_hierarchy = 'data_solicitacao'

    fieldsets = (
        ('🏢 Identificação da Empresa', {
            'fields': (
                'razao_social', 'nome_fantasia', 'cnpj', 'tipo_empresa',
                'site', 'instagram',
            )
        }),
        ('📍 Localização', {
            'fields': ('cep', 'endereco', 'cidade', 'estado'),
        }),
        ('👤 Responsável pelo Cadastro', {
            'fields': (
                'responsavel_nome', 'responsavel_cargo',
                'responsavel_email', 'responsavel_telefone',
            )
        }),
        ('💬 Sobre o Negócio', {
            'fields': ('descricao_negocio', 'capacidade', 'como_soube'),
        }),
        ('✅ Aceites Legais', {
            'fields': ('aceite_termos', 'aceite_privacidade', 'autoriza_contato', 'aceites_completos'),
        }),
        ('🔧 Controle Interno (Equipe Naviê)', {
            'fields': ('status', 'atendido_por', 'notas_internas', 'data_solicitacao', 'data_atualizacao'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Tipo')
    def tipo_empresa_badge(self, obj):
        colors = {
            'hotel_pousada': '#2563eb',
            'cinema': '#7c3aed',
            'casa_shows': '#db2777',
            'produtor_eventos': '#d97706',
            'restaurante': '#16a34a',
            'parque_turismo': '#0891b2',
            'outro': '#6b7280',
        }
        color = colors.get(obj.tipo_empresa, '#6b7280')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:99px;font-size:11px;font-weight:700;">{}</span>',
            color, obj.get_tipo_empresa_display()
        )

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {
            'pendente': '#f59e0b',
            'em_contato': '#2563eb',
            'aguardando_doc': '#7c3aed',
            'aprovado': '#16a34a',
            'recusado': '#dc2626',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:99px;font-size:11px;font-weight:700;">{}</span>',
            color, obj.get_status_display()
        )

    @admin.display(description='Aceites OK?', boolean=True)
    def aceites_ok(self, obj):
        return obj.aceites_completos


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'atualizado_em')
    readonly_fields = ('atualizado_em',)
    fields = ('slug', 'titulo', 'conteudo', 'atualizado_em')
