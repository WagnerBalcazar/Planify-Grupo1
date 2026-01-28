from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('eliminar-tarea/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),

    path('editar-tarea/<int:tarea_id>/', views.editar_tarea, name='editar_tarea'),

path('completar/<int:tarea_id>/', views.completar_tarea, name='completar_tarea'),

]