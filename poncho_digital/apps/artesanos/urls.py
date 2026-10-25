from django.urls import path
from . import views

app_name = 'artesanos'

urlpatterns = [
    path('registro/', views.registro_artesano, name='registro'),
    path('consultar-estado/', views.consultar_estado, name='consultar'),
]