from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.lista_productos, name='lista'),
    path('cargar/', views.cargar_producto, name='cargar'),
    path('mis_productos/', views.mis_productos, name='mis_productos'),
    path('editar/<int:pk>/', views.editar_producto, name='editar'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar'),
]