from django import forms
from .models import Actividad
from bienestar.models import EntradaGratitud

class TareaForm(forms.ModelForm):

    curso = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Matemáticas'})
    )
    lugar = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Aula 204'})
    )

    class Meta:
        model = Actividad

        fields = ['titulo', 'fecha_hora', 'prioridad', 'curso', 'lugar']

        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '¿Qué vas a hacer?'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
        }

class GratitudForm(forms.ModelForm):
    class Meta:
        model = EntradaGratitud
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }