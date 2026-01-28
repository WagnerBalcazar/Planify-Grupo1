from django.db import models
from django.contrib.auth.models import User
import random


class FrasePositiva(models.Model):
    texto = models.TextField()
    autor = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.texto[:50]


class ActividadAutocuidado(models.Model):
    nombre = models.CharField(max_length=100)  # Ej: "Respiración 4-7-8"
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class EstadoEmocional(models.Model):
    ESTADOS = [
        ('Feliz', '😊 Feliz'),
        ('Serio', '😐 Serio'),
        ('Triste', '😢 Triste'),
        ('Enojado', '😠 Enojado'),
        ('Ansioso', '😰 Ansioso'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    nivel = models.CharField(max_length=20, choices=ESTADOS)

    # Lógica RF08: Si es negativo, buscar sugerencia
    def obtener_sugerencia(self):
        if self.nivel in [ 'Serio', 'Triste', 'Enojado', 'Ansioso']:
            sugerencias = list(ActividadAutocuidado.objects.all())
            if sugerencias:
                return random.choice(sugerencias)
        return None


class EntradaGratitud(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    contenido = models.TextField()

    def __str__(self):
        return f"Gratitud de {self.usuario.username} - {self.fecha}"


from django.db import models

# Create your models here.
