from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

# MODELOS
from .models import Actividad, Tarea, Evento, Meta
from bienestar.models import EstadoEmocional, EntradaGratitud, FrasePositiva
from .forms import TareaForm, GratitudForm


# --- VISTA PRINCIPAL (DASHBOARD) ---
@login_required(login_url='login')
def dashboard(request):
    usuario = request.user

    # ==========================================
    # 1. PROCESAR FORMULARIOS (POST)
    # ==========================================
    if request.method == 'POST':
        if 'btn_actividad' in request.POST:
            tipo = request.POST.get('tipo_actividad')
            titulo = request.POST.get('titulo')
            fecha = request.POST.get('fecha')
            prioridad = request.POST.get('prioridad', 'MEDIA')

            # 1. VALIDACIÓN GENERAL: Título y Fecha OBLIGATORIOS para todos
            if not titulo or not fecha:
                messages.error(request, "⚠️ Error: El título y la fecha son obligatorios.")
                return redirect('dashboard')

            # Preparamos datos básicos
            datos_base = {
                'usuario': usuario,
                'titulo': titulo,
                'fecha_hora': fecha,
                'prioridad': prioridad,
                'completada': False,
                'descripcion': ''
            }

            try:
                # --- LÓGICA ESPECÍFICA SEGÚN TIPO ---

                if tipo == 'Tarea':
                    curso_input = request.POST.get('curso')
                    #  VALIDACIÓN ESTRICTA: Si no hay curso, NO se guarda
                    if not curso_input or curso_input.strip() == "":
                        messages.error(request, "⚠️ Error: Debes escribir la Materia o Curso.")
                        return redirect('dashboard')

                    Tarea.objects.create(**datos_base, curso=curso_input)
                    messages.success(request, " Tarea registrada correctamente.")

                elif tipo == 'Evento':
                    ubicacion_input = request.POST.get('ubicacion')
                    #  VALIDACIÓN ESTRICTA: Si no hay ubicación, NO se guarda
                    if not ubicacion_input or ubicacion_input.strip() == "":
                        messages.error(request, "⚠️ Error: Debes escribir la Ubicación del evento.")
                        return redirect('dashboard')

                    Evento.objects.create(**datos_base, lugar=ubicacion_input)
                    messages.success(request, " Evento registrado correctamente.")

                elif tipo == 'Meta':
                    avance_input = request.POST.get('nivel_avance')


                    # Si el campo viene vacío, asumimos que es 0.
                    if not avance_input:
                        avance_final = 0
                    else:
                        avance_final = avance_input

                    Meta.objects.create(
                        **datos_base,
                        estado='PENDIENTE',
                        nivel_avance=avance_final
                    )
                    messages.success(request, " Meta establecida (Avance inicial: " + str(avance_final) + "%).")

            except Exception as e:
                # Capturamos cualquier otro error raro (ej. fecha inválida en DB)
                messages.error(request, f"Ocurrió un error inesperado: {e}")

            return redirect('dashboard')

    # ==========================================
    # 2. PREPARAR DATOS PARA VER (GET)
    # ==========================================

    # A) Lógica de Tareas
    todas_actividades = Actividad.objects.filter(usuario=usuario).select_related('tarea', 'evento', 'meta').order_by(
        'fecha_hora')
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

    # B) Gratitud
    mi_gratitud = EntradaGratitud.objects.filter(usuario=usuario).order_by('-fecha')[:10]

    # C) Frase Positiva
    frase_obj = FrasePositiva.objects.order_by('?').first()
    if frase_obj:
        texto_frase = frase_obj.texto

    else:
        texto_frase = "Cada paso cuenta, sigue adelante."
        autor_frase = "Planify"

    # D) Contexto final
    context = {
        'usuario': usuario,
        'mis_tareas': pendientes,
        'historial': historial[:5],
        'mi_gratitud': mi_gratitud,
        'hoy': timezone.now(),
        'frase': texto_frase,

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

    frase_random = FrasePositiva.objects.order_by('?').first()
    mensaje = f"Excelente. {frase_random.texto}" if frase_random else "Actividad completada."

    messages.success(request, mensaje)
    return redirect('dashboard')


# --- ELIMINAR ---
@login_required
def eliminar_tarea(request, tarea_id):
    actividad = get_object_or_404(Actividad, id=tarea_id, usuario=request.user)
    actividad.delete()
    messages.error(request, "Se eliminó correctamente.")
    return redirect('dashboard')


# --- EDICIÓN ---
@login_required
def editar_tarea(request, tarea_id):
    actividad = get_object_or_404(Actividad, id=tarea_id, usuario=request.user)

    if request.method == 'POST':
        form = TareaForm(request.POST, instance=actividad)
        if form.is_valid():
            actividad_guardada = form.save()

            if actividad_guardada.tipo_real == 'Tarea':
                actividad_guardada.tarea.curso = form.cleaned_data.get('curso')
                actividad_guardada.tarea.save()

            elif actividad_guardada.tipo_real == 'Evento':
                actividad_guardada.evento.lugar = form.cleaned_data.get('lugar')
                actividad_guardada.evento.save()

            elif actividad_guardada.tipo_real == 'Meta':
                nuevo_avance = request.POST.get('nivel_avance')
                if nuevo_avance:
                    actividad_guardada.meta.nivel_avance = int(nuevo_avance)
                    actividad_guardada.meta.save()

            messages.success(request, "Actualizado correctamente.")
            return redirect('dashboard')
    else:
        initial_data = {}
        if actividad.tipo_real == 'Tarea':
            initial_data['curso'] = actividad.tarea.curso
        elif actividad.tipo_real == 'Evento':
            initial_data['lugar'] = actividad.evento.lugar

        form = TareaForm(instance=actividad, initial=initial_data)

    return render(request, 'gestion_actividades/editar_item.html', {
        'form': form,
        'actividad': actividad,
        'titulo': f'Editar {actividad.tipo_real}'
    })