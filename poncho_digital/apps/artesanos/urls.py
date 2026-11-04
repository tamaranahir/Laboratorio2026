from django.urls import path
from . import views

app_name = 'artesanos'

urlpatterns = [
    path('registro/', views.registro_artesano, name='registro'),
    path('consultar-estado/', views.consultar_estado, name='consultar'),
    path('mi-stand/', views.mi_stand, name='mi_stand'),
    path('gestion-stands/', views.gestion_stands, name='gestion_stands'),
    path('gestion-stands/editar/<int:stand_id>/', views.editar_stand, name='editar_stand'),
    path('gestion-stands/eliminar/<int:stand_id>/', views.eliminar_stand, name='eliminar_stand'),
    path('evaluar/', views.evaluar_solicitudes, name='evaluar_solicitudes'),
    path('evaluar/<int:pk>/<str:nuevo_estado>/', views.cambiar_estado_solicitud, name='cambiar_estado_solicitud'),
]