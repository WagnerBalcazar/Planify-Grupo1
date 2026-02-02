from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages


# --- VISTA DE REGISTRO
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})


# --- VISTA DE LOGIN
def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        else:
            # Si el formulario no es válido es porque las credenciales fallaron
            messages.error(request, "Usuario o contraseña incorrectos. Inténtalo de nuevo.")
    else:
        form = AuthenticationForm()

    return render(request, 'usuarios/login.html', {'form': form})