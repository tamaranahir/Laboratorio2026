from django.db import models
from apps.artesanos.models import Artesano

# 1. Tabla de Categorías de productos
class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def str(self):
        return self.nombre

# 2. Catálogo de piezas artesanales
class Producto(models.Model):

    # Relación: Cada producto pertenece a un Artesano
    artesano = models.ForeignKey(Artesano, on_delete=models.CASCADE, related_name="productos")
    # Relación: Cada producto tiene una Categoría
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos")

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    imagen = models.FileField(upload_to = 'productos', blank = True, null = True, verbose_name = "Foto del Producto")
    activo = models.BooleanField(default=True, verbose_name="¿Publicar inmediatamente?")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def str(self):
        return f"{self.titulo} - ${self.precio}"