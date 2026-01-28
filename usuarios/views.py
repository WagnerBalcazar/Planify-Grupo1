from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el usuario en la BD
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}! Ya puedes iniciar sesión.')
            return redirect('login')  # Lo mandamos al login
    else:
        form = UserCreationForm()

    return render(request, 'usuarios/registro.html', {'form': form})


from django.shortcuts import render

# Create your views here.
