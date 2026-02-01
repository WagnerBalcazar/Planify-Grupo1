document.addEventListener('DOMContentLoaded', function() {

    // ==========================================
    // 1. CARGAR DATOS (JSON)
    // ==========================================
    const dataScript = document.getElementById('data-tareas');
    if (dataScript) {
        try {
            window.misTareasJS = JSON.parse(dataScript.textContent);
        } catch (e) {
            console.error("Error leyendo JSON de tareas", e);
            window.misTareasJS = [];
        }
    } else {
        window.misTareasJS = [];
    }

    // ==========================================
    // 2. INICIALIZAR FUNCIONES
    // ==========================================

    inicializarFormularioDinamico(); // <- Esta activa las burbujas
    renderCalendar();

    // Alertas de Borrado y Límites de texto
    inicializarSweetAlert();
    inicializarControlLimites();

    // Auto-eliminar mensajes de Django (éxito/error)
    setTimeout(function() {
        const mensajes = document.querySelectorAll('.notificacion, .mensaje-exito, .alert');
        mensajes.forEach(function(msg) {
            msg.style.transition = "opacity 0.5s ease";
            msg.style.opacity = "0";
            setTimeout(function() { msg.remove(); }, 500);
        });
    }, 5000);

    // ==========================================
    // 3. LÓGICA TEMA OSCURO
    // ==========================================
    const btnTema = document.getElementById('btnTema');
    if(btnTema){
        btnTema.addEventListener('click', () => {
            const html = document.documentElement;
            if (html.getAttribute('data-theme') === 'dark') {
                html.removeAttribute('data-theme');
                localStorage.setItem('temaPlanify', 'light');
                btnTema.innerHTML = '<i class="fas fa-moon"></i>';
            } else {
                html.setAttribute('data-theme', 'dark');
                localStorage.setItem('temaPlanify', 'dark');
                btnTema.innerHTML = '<i class="fas fa-sun"></i>';
            }
        });
    }
});


// ==========================================
// 4. FORMULARIO DINÁMICO (LA MAGIA DE LAS BURBUJAS)
// ==========================================
function inicializarFormularioDinamico() {
    const selector = document.getElementById('tipoSelector');
    const inputCurso = document.getElementById('inputCurso');
    const inputUbicacion = document.getElementById('inputUbicacion');
    const inputAvance = document.getElementById('inputAvance');

    if (selector) {
        function actualizarFormulario() {
            const tipo = selector.value;

            // 1. Ocultar todo y quitar 'required' para evitar errores falsos
            [inputCurso, inputUbicacion, inputAvance].forEach(el => {
                if(el) {
                    el.style.display = 'none';
                    el.required = false; // Importante: Quitamos la obligación
                }
            });

            // 2. Mostrar y hacer OBLIGATORIO según el caso
            if (tipo === 'Tarea' && inputCurso) {
                inputCurso.style.display = 'block';
                inputCurso.required = true; // Activa la burbuja si está vacío
                inputCurso.placeholder = "Nombre de la materia (Obligatorio)";
            }
            else if (tipo === 'Evento' && inputUbicacion) {
                inputUbicacion.style.display = 'block';
                inputUbicacion.required = true; // Activa la burbuja si está vacío
                inputUbicacion.placeholder = "Ubicación (Obligatorio)";
            }
            else if (tipo === 'Meta' && inputAvance) {
                inputAvance.style.display = 'block';
                inputAvance.required = false; // Meta permite vacío (es 0 en backend)
            }
        }

        selector.addEventListener('change', actualizarFormulario);
        // Ejecutar al inicio para asegurar estado correcto
        actualizarFormulario();
    }
}


// ==========================================
// 5. FUNCIONES DE INTERFAZ (Acordeón, Paneles)
// ==========================================

function toggleAccordion(element) {
    if (!element) return;

    // Si hago clic en el mismo que ya está abierto, lo cierro
    const yaEstabaActivo = element.classList.contains('active');

    // Cerrar todos primero
    document.querySelectorAll('.input-card').forEach(card => {
        card.classList.remove('active');
        const icon = card.querySelector('.toggle-icon');
        if (icon) icon.style.transform = 'rotate(0deg)';
        const content = card.querySelector('.form-content');
        if(content) content.style.display = 'none';
    });

    // Si no estaba activo, lo abrimos
    if (!yaEstabaActivo) {
        element.classList.add('active');
        const icon = element.querySelector('.toggle-icon');
        if (icon) icon.style.transform = 'rotate(180deg)';
        const content = element.querySelector('.form-content');
        if(content) content.style.display = 'block';
    }
}

function stopProp(event) {
    // Evita que al hacer clic en un input se cierre el acordeón
    event.stopPropagation();
}

function mostrarLista(idPanel) {
    // Ocultar todos los paneles
    document.querySelectorAll('.list-section').forEach(sec => {
        sec.classList.remove('active-panel');
        sec.style.display = 'none';
    });

    // Mostrar el seleccionado
    const panel = document.getElementById(idPanel);
    if (panel) {
        panel.style.display = 'block';
        // Timeout pequeño para permitir animación CSS si existe
        setTimeout(() => panel.classList.add('active-panel'), 10);

        // Si es el calendario, redibujarlo para que se ajuste bien
        if(idPanel === 'vistaCalendario') {
            renderCalendar();
        }
    }
}


// ==========================================
// 6. CALENDARIO (MODIFICADO PARA TEXTO)
// ==========================================
let currentDate = new Date();

function renderCalendar() {
    const grid = document.getElementById('gridDias');
    const mesAnio = document.getElementById('mesAnio');
    if (!grid) return;

    grid.innerHTML = '';
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    const meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
    if(mesAnio) mesAnio.innerText = `${meses[month]} ${year}`;

    const firstDay = new Date(year, month, 1).getDay();
    const lastDay = new Date(year, month + 1, 0).getDate();

    // Rellenar espacios vacíos al inicio
    for (let i = 0; i < firstDay; i++) {
        grid.innerHTML += '<div class="calendar-day empty"></div>';
    }

    // Dibujar días
    for (let i = 1; i <= lastDay; i++) {
        const dayDiv = document.createElement('div');
        dayDiv.classList.add('calendar-day');

        // Agregamos el número del día
        const numDiv = document.createElement('div');
        numDiv.className = 'day-number';
        numDiv.innerText = i;
        dayDiv.appendChild(numDiv);

        // Formato fecha YYYY-MM-DD
        const mesStr = (month + 1).toString().padStart(2, '0');
        const diaStr = i.toString().padStart(2, '0');
        const fechaStr = `${year}-${mesStr}-${diaStr}`;

        // Filtrar tareas de este día
        const tareasDelDia = (window.misTareasJS || []).filter(t => t.fecha === fechaStr);

        // --- AQUÍ ESTÁ EL CAMBIO: DE PUNTOS A TEXTO ---
        if (tareasDelDia.length > 0) {
            dayDiv.classList.add('has-task');

            tareasDelDia.forEach(t => {
                // Creamos un DIV en lugar de un SPAN para que sea una barra
                const label = document.createElement('div');

                // Asignamos clase base 'task-label' y el tipo (tarea, evento, meta)
                // Usamos toLowerCase() para evitar errores si viene en Mayúsculas
                label.className = `task-label ${t.tipo.toLowerCase()}`;

                // PONEMOS EL TEXTO VISIBLE
                label.innerText = t.titulo;

                // Tooltip (al pasar el mouse se ve completo)
                label.title = t.titulo;

                dayDiv.appendChild(label);
            });
        }
        grid.appendChild(dayDiv);
    }
}

function cambiarMes(delta) {
    currentDate.setMonth(currentDate.getMonth() + delta);
    renderCalendar();
}
// ==========================================
// 7. UTILIDADES (Límites de texto y Alerta Borrar)
// ==========================================
function inicializarControlLimites() {
    const inputsConLimite = document.querySelectorAll('.input-limitado');
    inputsConLimite.forEach(input => {
        input.addEventListener('input', function() {
            const maximo = this.getAttribute('maxlength');
            if (this.value.length >= maximo) {
                const Toast = Swal.mixin({
                    toast: true, position: 'top-end', showConfirmButton: false, timer: 2000, timerProgressBar: true
                });
                Toast.fire({ icon: 'warning', title: '¡Llegaste al límite de texto!' });
            }
        });
    });
}

function inicializarSweetAlert() {
    // Solo para botones de ELIMINAR, no para validar formulario
    const botones = document.querySelectorAll('.btn-eliminar-sweet');
    if (botones.length > 0) {
        botones.forEach(boton => {
            boton.addEventListener('click', function(e) {
                e.preventDefault();
                const urlDestino = e.currentTarget.getAttribute('href');
                const esOscuro = document.documentElement.getAttribute('data-theme') === 'dark';

                Swal.fire({
                    title: '¿Eliminar?',
                    text: "¿Seguro que deseas eliminarlo?",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#d33',
                    cancelButtonColor: '#6c757d',
                    confirmButtonText: 'Eliminar',
                    cancelButtonText: 'Cancelar',
                    background: esOscuro ? '#2c0b0e' : '#fff',
                    color: esOscuro ? '#ffcccc' : '#5a1e1e'
                }).then((result) => {
                    if (result.isConfirmed && urlDestino) {
                        window.location.href = urlDestino;
                    }
                });
            });
        });
    }
}