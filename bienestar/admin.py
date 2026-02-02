from django.contrib import admin
from .models import EstadoEmocional, EntradaGratitud, FrasePositiva, ActividadAutocuidado

@admin.register(EstadoEmocional)
class EstadoEmocionalAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nivel', 'fecha')
    list_filter = ('nivel',)

@admin.register(EntradaGratitud)
class GratitudAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha', 'contenido_corto')

    def contenido_corto(self, obj):
        return obj.contenido[:50]

# Registros  para configuración
admin.site.register(FrasePositiva)
admin.site.register(ActividadAutocuidado)