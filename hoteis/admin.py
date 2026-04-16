from django.contrib import admin
from .models import Produtor, Local, Hotel, HotelImagem, Quarto

class HotelImagemInline(admin.TabularInline):
    model = HotelImagem
    extra = 1

class QuartoInline(admin.TabularInline):
    model = Quarto
    extra = 1

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('nome', 'local', 'status', 'destaque', 'data_inicio')
    list_filter = ('status', 'destaque')
    search_fields = ('nome', 'local__nome')
    inlines = [HotelImagemInline, QuartoInline]

admin.site.register(Produtor)
admin.site.register(Local)
