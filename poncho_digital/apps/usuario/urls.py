from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuario'

urlpatterns = [
    # Login nativo de Django
    path('login/', auth_views.LoginView.as_view(template_name='usuario/login.html'), name='login'),
    # Logout nativo de Django
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.salir, name='logout'),
]