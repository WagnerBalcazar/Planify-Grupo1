from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

# MODELOS
from .models import Actividad, Tarea, Evento, Meta
from bienestar.models import EstadoEmocional, EntradaGratitud, FrasePositiva # Mantenemos import para lectura
from .forms import TareaForm, GratitudForm

# --- VISTA DEL DASHBOARD ---
@login_required(login_url='login')
def dashboard(request):
    usuario = request.user

    # ==========================================
    # 1. PROCESAR FORMULARIOS (SOLO LOGÍSTICA)
    # ==========================================
    if request.method == 'POST':
        # GUARDAR ACTIVIDAD (Tarea, Evento, Meta)
        if 'btn_actividad' in request.POST:
            tipo = request.POST.get('tipo_actividad')
            titulo = request.POST.get('titulo')
            fecha = request.POST.get('fecha')
            prioridad = request.POST.get('prioridad', 'MEDIA')

            curso_input = request.POST.get('curso')
            ubicacion_input = request.POST.get('ubicacion')

            datos_base = {
                'usuario': usuario,
                'titulo': titulo,
                'fecha_hora': fecha,
                'prioridad': prioridad,
                'completada': False,
                'descripcion': ''
            }

            if tipo == 'Tarea':
                Tarea.objects.create(**datos_base, curso=curso_input)
                messages.success(request, "Tarea registrada.")

            elif tipo == 'Evento':
                Evento.objects.create(**datos_base, lugar=ubicacion_input)
                messages.success(request, "Evento registrado.")

            elif tipo == 'Meta':
                avance_ingresado = request.POST.get('nivel_avance') or 0
                Meta.objects.create(
                    **datos_base,
                    estado='PENDIENTE',
                    nivel_avance=avance_ingresado
                )
                messages.success(request, "Meta establecida.")

            return redirect('dashboard')

    # ==========================================
    # 2. PREPARAR DATOS PARA VER (GET)
    # ==========================================
    todas_actividades = Actividad.objects.filter(usuario=usuario).select_related('tarea', 'evento', 'meta').order_by('fecha_hora')

    pendientes = []
    historial = []

    for item in todas_actividades:
        if item.completada:
            historial.append(item)
        else:
            if item.tipo_real == 'Meta' and item.meta.estado == 'FINALIZADA':
                historial.append(item)
            else:
                pendientes.append(item)

    historial.reverse()

    # Seguimos trayendo estos datos de la app bienestar para mostrarlos en el HTML
    mi_gratitud = EntradaGratitud.objects.filter(usuario=usuario).order_by('-fecha')[:10]

    context = {
        'usuario': usuario,
        'mis_tareas': pendientes,
        'historial': historial[:5],
        'mi_gratitud': mi_gratitud,
        'hoy': timezone.now(),
    }
    return render(request, 'gestion_actividades/dashboard.html', context)


# --- COMPLETAR TAREA ---
@login_required(login_url='login')
def completar_tarea(request, tarea_id):
    actividad = get_object_or_404(Actividad, id=tarea_id, usuario=request.user)
    actividad.completada = True
    actividad.save()

    if hasattr(actividad, 'meta'):
        actividad.meta.marcar_como_finalizada()

    # Buscamos frase de bienestar para motivar
    frase_random = FrasePositiva.objects.order_by('?').first()
    mensaje = f"Excelente. {frase_random.texto}" if frase_random else "Actividad completada."

    messages.success(request, mensaje)
    return redirect('dashboard')

# --- ELIMINAR ---
@login_required
def eliminar_tarea(request, tarea_id):
    actividad = get_object_or_404(Actividad, id=tarea_id, usuario=request.user)
    actividad.delete()
    messages.warning(request, "Elemento eliminado.")
    return redirect('dashboard')


# --- EDICIÓN ---
@login_required
def editar_tarea(request, tarea_id):
    actividad = get_object_or_404(Actividad, id=tarea_id, usuario=request.user)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=actividad)
        if form.is_valid():
            actividad_guardada = form.save()
            if actividad_guardada.tipo_real == 'Meta':
                nuevo_avance = request.POST.get('nivel_avance')
                if nuevo_avance:
                    actividad_guardada.meta.nivel_avance = int(nuevo_avance)
                    actividad_guardada.meta.save()
            messages.success(request, "Actualizado correctamente.")
            return redirect('dashboard')
    else:
        form = TareaForm(instance=actividad)
    return render(request, 'gestion_actividades/editar_item.html', {'form': form, 'titulo': f'Editar {actividad.tipo_real}'})

