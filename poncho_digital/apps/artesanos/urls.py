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
    path('rubros/', views.gestion_rubros, name='gestion_rubros'),
    path('rubros/editar/<int:pk>/', views.editar_rubro, name='editar_rubro'),
    path('rubros/eliminar/<int:pk>/', views.eliminar_rubro, name='eliminar_rubro'),
    path('reportes/', views.panel_reportes, name='panel_reportes'),
#🚨  NUEVA URL -AGREGAR VALE#
    path('reportes/', views.panel_reportes, name='panel_reportes'),
    path('artesano/<int:artesano_id>/consultar/', views.enviar_consulta, name='enviar_consulta'),
    path('mis-consultas/', views.mis_consultas, name='mis_consultas'),
    path('panel-artesano/consultas/', views.consultas_recibidas, name='consultas_recibidas'),
    path('panel-artesano/consultas/<int:consulta_id>/responder/', views.responder_consulta, name='responder_consulta'),
]