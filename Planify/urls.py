from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from usuarios import views as user_views  # Tus vistas personalizadas

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. LOGIN (Usamos tu nueva vista 'login_view')
    path('login/', user_views.login_view, name='login'),

    # 2. LOGOUT (Usamos la de Django, redirige al login al salir)
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # 3. REGISTRO (CORREGIDO: Apunta a tu vista 'registro_view')
    path('registro/', user_views.registro_view, name='registro'),

    # 4. TUS OTRAS APPS
    path('', include('gestion_actividades.urls')),
    path('bienestar/', include('bienestar.urls')),
]