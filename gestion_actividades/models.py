from django.db import models
from django.conf import settings
from django.apps import apps


# 1. CLASE : ACTIVIDAD
class Actividad(models.Model):
    PRIORIDAD_CHOICES = [
        ('ALTA', 'Alta'),
        ('MEDIA', 'Media'),
        ('BAJA', 'Baja'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='MEDIA')
    fecha_hora = models.DateTimeField()


    # Movemos esto aquí para que TODOS (Eventos, Tareas) puedan tener check
    completada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titulo} ({self.prioridad})"

    @property
    def tipo_real(self):
        if hasattr(self, 'tarea'): return 'Tarea'
        if hasattr(self, 'evento'): return 'Evento'
        if hasattr(self, 'meta'): return 'Meta'
        return 'Actividad'


# 2. CLASE HIJA: TAREA
class Tarea(Actividad):
    # Ya no necesitamos 'completada' aquí, lo hereda del padre
    curso = models.CharField(max_length=100, blank=True, null=True)


# 3. CLASE HIJA: EVENTO
class Evento(Actividad):
    lugar = models.CharField(max_length=200, blank=True, null=True)


# 4. CLASE META
class Meta(Actividad):
    # Meta es especial, mantiene su estado interno, pero usaremos 'completada' para el historial
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROGRESO', 'En progreso'),
        ('FINALIZADA', 'Finalizada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    nivel_avance = models.PositiveIntegerField(default=0)

    def marcar_como_finalizada(self):
        self.estado = 'FINALIZADA'
        self.nivel_avance = 100
        self.completada = True  # También marcamos el check general
        self.save()
