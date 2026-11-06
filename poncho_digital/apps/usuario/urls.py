
from django.urls import path
from . import views

app_name = 'usuario'

urlpatterns = [
    
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.salir, name='logout'),
    path('registro/', views.registro_usuario, name='registro'),
]