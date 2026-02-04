from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistroUsuarioForm, EmailAuthenticationForm


# --- VISTA DE REGISTRO ---
def registro_view(request):
    # Si el usuario ya está logueado, lo mandamos al dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Opción A: Auto-login y mandar al dashboard (comentado)
            # login(request, user)
            # return redirect('dashboard')

            # Opción B: Mandarlo al login para que entre con su cuenta (ACTIVA)
            messages.success(request, f"¡Cuenta creada! Bienvenido, {user.first_name}. Por favor inicia sesión.")
            return redirect('login')

    else:
        form = RegistroUsuarioForm()

    return render(request, 'usuarios/registro.html', {'form': form})


# --- VISTA DE LOGIN ---
def login_view(request):
    # Si ya está logueado, no debe ver el login, va al dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # --- CORRECCIÓN CLAVE ---
            # Aquí es donde tenías el error. Antes decía 'inicio', ahora 'dashboard'.
            return redirect('dashboard')

    else:
        form = EmailAuthenticationForm()

    return render(request, 'usuarios/login.html', {'form': form})


# --- VISTA DE CERRAR SESIÓN (LOGOUT) ---
def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('login')


# --- VISTA DEL DASHBOARD (PANEL PRINCIPAL) ---
@login_required  # Esto protege la vista: si no estás logueado, no entras
def dashboard_view(request):
    return render(request, 'usuarios/dashboard.html')