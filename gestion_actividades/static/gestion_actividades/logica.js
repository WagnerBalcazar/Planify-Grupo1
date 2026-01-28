// --- FUNCIONES GLOBALES (Deben estar fuera para que el HTML las vea) ---

function stopProp(event) {
    if (event) event.stopPropagation();
}

function toggleAccordion(element) {
    // Si el clic viene de un elemento interactivo, no cerramos
    if (event.target.tagName === 'BUTTON' ||
        event.target.tagName === 'INPUT' ||
        event.target.tagName === 'TEXTAREA' ||
        event.target.closest('form')) {
        return;
    }

    const allCards = document.querySelectorAll('.input-card');
    const isActive = element.classList.contains('active');

    allCards.forEach(card => card.classList.remove('active'));

    if (!isActive) {
        element.classList.add('active');
    }
}

// --- LÓGICA AL CARGAR EL DOCUMENTO ---
document.addEventListener("DOMContentLoaded", function() {

    // 1. MODO OSCURO
    const btnTema = document.getElementById('btnTema');
    const icon = btnTema ? btnTema.querySelector('i') : null;

    if (btnTema && icon) {
        const temaGuardado = localStorage.getItem('temaPlanify');

        if (temaGuardado === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
            icon.classList.replace('fa-moon', 'fa-sun');
        }

        btnTema.addEventListener('click', () => {
            const esOscuro = document.documentElement.getAttribute('data-theme') === 'dark';
            if (esOscuro) {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('temaPlanify', 'light');
                icon.classList.replace('fa-sun', 'fa-moon');
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('temaPlanify', 'dark');
                icon.classList.replace('fa-moon', 'fa-sun');
            }
        });
    }

    // 2. MOSTRAR PANELES (TAREAS / GRATITUD)
    window.mostrarLista = function(idLista) {
        const bienvenida = document.getElementById('panelBienvenida');
        if (bienvenida) bienvenida.style.display = 'none';

        document.querySelectorAll('.list-section').forEach(sec => {
            sec.style.display = 'none';
            sec.classList.remove('active-panel');
        });

        const lista = document.getElementById(idLista);
        if (lista) {
            lista.style.display = 'block';
            setTimeout(() => lista.classList.add('active-panel'), 10);
        }
    };

    // 3. INPUT DINÁMICO (TAREA / EVENTO / META)
    const tipoSelector = document.getElementById('tipoSelector');
    if (tipoSelector) {
        tipoSelector.addEventListener('change', function() {
            document.querySelectorAll('.input-dinamico').forEach(el => el.style.display = 'none');
            if (this.value === 'Tarea') document.getElementById('inputCurso').style.display = 'block';
            else if (this.value === 'Evento') document.getElementById('inputUbicacion').style.display = 'block';
            else if (this.value === 'Meta') document.getElementById('inputAvance').style.display = 'block';
        });
    }

    // 4. AUTO-ABRIR PANEL SI VIENE DE GUARDAR
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('saved') || urlParams.get('open') === 'gratitud') {
        // Buscamos el panel que contiene el botón de "Ver mi Diario"
        const btnGratitud = document.querySelector('button[onclick*="listaGratitud"]');
        if (btnGratitud) {
            const card = btnGratitud.closest('.input-card');
            if (card) {
                card.classList.add('active');
                window.mostrarLista('listaGratitud'); // Opcional: muestra la lista directo
            }
        }
    }

});
// --- AUTO-OCULTAR MENSAJES DE ÉXITO ---
window.addEventListener('DOMContentLoaded', () => {
    // Buscamos todos los mensajes que tengan la clase 'mensaje-exito'
    const mensajes = document.querySelectorAll('.mensaje-exito');

    mensajes.forEach(msg => {
        // Esperar 4 segundos y luego desvanecer
        setTimeout(() => {
            msg.style.transition = "opacity 0.5s ease";
            msg.style.opacity = "0";

            // Borrar el elemento del mapa después de la animación
            setTimeout(() => {
                msg.remove();
            }, 500);
        }, 4000); // 4000ms = 4 segundos
    });
});