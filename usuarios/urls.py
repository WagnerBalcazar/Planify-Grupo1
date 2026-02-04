from django.urls import path
from . import views

urlpatterns = [
    # ... tus otras rutas ...
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_usuario, name='login'),
]