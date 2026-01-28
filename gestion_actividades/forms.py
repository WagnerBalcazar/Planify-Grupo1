from django import forms

# 1. Importamos Actividad desde ESTA aplicación (.models)
from .models import Actividad

# 2. Importamos EntradaGratitud desde la aplicación BIENESTAR
from bienestar.models import EntradaGratitud

class TareaForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['titulo', 'fecha_hora', 'prioridad', 'descripcion']
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '¿Qué vas a hacer?'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Detalles opcionales...'}),
        }

class GratitudForm(forms.ModelForm):
    class Meta:
        model = EntradaGratitud
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }