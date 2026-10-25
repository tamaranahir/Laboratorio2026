from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'artesano', 'categoria', 'precio', 'stock', 'activo', 'fecha_creacion')
    list_filter = ('categoria', 'activo')
    search_fields = ('nombre', 'descripcion', 'artesano__nombre_completo')