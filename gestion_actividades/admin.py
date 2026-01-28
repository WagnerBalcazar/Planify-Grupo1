from django.contrib import admin
# Importamos las 4 clases nuevas
from .models import Actividad, Tarea, Evento, Meta


# 1. Configuración para TAREAS
@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    # Mostramos columnas específicas de tareas (como el curso)
    list_display = ('titulo', 'prioridad', 'fecha_hora', 'completada', 'curso')
    list_filter = ('prioridad', 'completada')
    search_fields = ('titulo', 'curso')


# 2. Configuración para EVENTOS
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    # Mostramos el LUGAR, que es exclusivo de eventos
    list_display = ('titulo', 'prioridad', 'fecha_hora', 'lugar')
    list_filter = ('prioridad',)
    search_fields = ('titulo', 'lugar')


# 3. Configuración para METAS
@admin.register(Meta)
class MetaAdmin(admin.ModelAdmin):
    # Mostramos estado y avance
    list_display = ('titulo', 'prioridad', 'estado', 'nivel_avance')
    list_filter = ('estado',)


# 4. Configuración para ver TODAS las actividades juntas (Padre)
@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo_real', 'prioridad', 'fecha_hora')
    list_filter = ('prioridad',)

    # Esta función permite ver en el admin si es Tarea, Evento o Meta
    def tipo_real(self, obj):
        return obj.tipo_real

    tipo_real.short_description = 'Tipo de Actividad'