from django.db import models
from apps.artesanos.models import Artesano

# 1. Categorías de productos (Textil, Cerámica, Cestería, etc.)
class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True, verbose_name="Nombre de Categoría")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


# 2. Catálogo de productos
class Producto(models.Model):
    artesano = models.ForeignKey(Artesano, on_delete=models.CASCADE, related_name="productos", verbose_name="Artesano")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos", verbose_name="Categoría")

    nombre = models.CharField(max_length=150, verbose_name="Nombre del Producto")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    stock = models.PositiveIntegerField(default=1, verbose_name="Stock")
    imagen = models.FileField(upload_to='productos/', blank=True, null=True, verbose_name="Foto del Producto")
    activo = models.BooleanField(default=True, verbose_name="¿Publicar inmediatamente?")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"