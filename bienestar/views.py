from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EstadoEmocional, EntradaGratitud
# Asegúrate de que el Form esté disponible (puedes mover el form a bienestar o importarlo así)
from gestion_actividades.forms import GratitudForm


@login_required
def registrar_emocion(request):
    """Procesa la selección de emojis y devuelve sugerencias de autocuidado."""
    if request.method == "POST":
        nivel = request.POST.get('emocion_seleccionada')

        # 1. Creamos el registro en la BD
        nuevo_estado = EstadoEmocional.objects.create(
            usuario=request.user,
            nivel=nivel
        )

        # 2. Obtenemos sugerencia del modelo (RF08)
        sugerencia = nuevo_estado.obtener_sugerencia()

        if nivel == 'Feliz':
            messages.success(request, " Sigue contagiando esa energía.")
        elif sugerencia:
            # Mensaje azul con el consejo de la base de datos
            messages.info(request, f"  Sugerencia: {sugerencia.nombre} - {sugerencia.descripcion}")
        else:
            # Si no hay actividades en la BD o es un estado neutro
            messages.success(request, "Estado de ánimo registrado correctamente.")

    return redirect('dashboard')


def registrar_gratitud(request):
    if request.method == "POST":
        contenido = request.POST.get('contenido_gratitud')
        if contenido:
            EntradaGratitud.objects.create(usuario=request.user, contenido=contenido)
            messages.success(request, "¡Guardado con éxito! 🙏")

    # Redirigir al dashboard
    return redirect('dashboard')

@login_required
def editar_gratitud(request, entrada_id):
    """Permite editar una nota del diario desde la app bienestar."""
    entrada = get_object_or_404(EntradaGratitud, id=entrada_id, usuario=request.user)

    if request.method == 'POST':
        form = GratitudForm(request.POST, instance=entrada)
        if form.is_valid():
            form.save()
            messages.success(request, "Entrada del diario actualizada con éxito.")
            return redirect('dashboard')
    else:
        form = GratitudForm(instance=entrada)

    # Reutilizamos el template de edición que ya tienes en gestión
    return render(request, 'gestion_actividades/editar_item.html', {
        'form': form,
        'titulo': 'Editar Diario de Gratitud'
    })


@login_required
def eliminar_gratitud(request, entrada_id):
    """Borra una entrada del diario."""
    entrada = get_object_or_404(EntradaGratitud, id=entrada_id, usuario=request.user)
    entrada.delete()
    messages.warning(request, "Entrada eliminada correctamente.")
    return redirect('dashboard')