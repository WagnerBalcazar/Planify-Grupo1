from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from usuarios import views as user_views  # <--- Aquí están tus vistas

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- CAMBIO CRÍTICO AQUÍ ---
    # BORRA la línea de auth_views.LoginView y pon esta:
    path('login/', user_views.login_usuario, name='login'),

    # Esta de logout está bien, déjala así si quieres
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('registro/', user_views.registro, name='registro'),

    path('', include('gestion_actividades.urls')),
    path('bienestar/', include('bienestar.urls')),
]