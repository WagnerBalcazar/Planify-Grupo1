from django.urls import path
from . import views

# bienestar/urls.py
urlpatterns = [
    path('registrar-emocion/', views.registrar_emocion, name='registrar_emocion'),
    path('registrar-gratitud/', views.registrar_gratitud, name='registrar_gratitud'),
    path('eliminar-gratitud/<int:entrada_id>/', views.eliminar_gratitud, name='eliminar_gratitud'),
    path('editar-gratitud/<int:entrada_id>/', views.editar_gratitud, name='editar_gratitud'),
]