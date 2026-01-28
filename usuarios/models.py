from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    # Relación 1 a 1 con el usuario de Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=20, unique=True, null=True, blank=True)
    biografia = models.TextField(blank=True, verbose_name="Biografía")

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


from django.db import models

# Create your models here.
