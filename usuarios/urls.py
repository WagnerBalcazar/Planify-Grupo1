from django.urls import path
from . import views  # Importa tu archivo views.py donde está la lógica

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    # AQUÍ vinculamos tu función con la dirección /login/
    path('login/', views.login_usuario, name='login'),
]