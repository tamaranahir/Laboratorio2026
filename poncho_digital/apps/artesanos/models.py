from django.db import models
from django.contrib.auth.models import User

# 1. Tabla de Rubros
class Rubro(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Rubro")
    descripcion = models.TextField(blank=True, verbose_name="Descripción del Rubro")

    class Meta:
        verbose_name = "Rubro"
        verbose_name_plural = "Rubros"

    def __str__(self):
        return self.nombre

# 2. Puestos en el Predio Ferial
class Stand(models.Model):
    numero = models.PositiveIntegerField(unique=True, verbose_name="Número de Stand")
    pabellon = models.CharField(max_length=50, verbose_name="Pabellón")
    artesano = models.OneToOneField('Artesano', on_delete=models.SET_NULL, null=True, blank=True, related_name='stand')

    class Meta:
        verbose_name = "Stand"
        verbose_name_plural = "Stands"

    def __str__(self):
        estado = f"Ocupado por {self.artesano.nombre_marca}" if self.artesano and self.artesano.nombre_marca else "Disponible"
        return f"Stand {self.numero} - {self.pabellon} ({estado})"


# 3. Postulación y Perfil del Artesano
class Artesano(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente de Evaluación'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    )

    # Relación opcional con la cuenta de usuario de Django
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True,
        related_name="artesano", verbose_name="Cuenta de Usuario"
    )

    # Datos Personales
    nombre_completo = models.CharField(max_length=150, verbose_name="Nombre Completo")
    dni = models.CharField(max_length=10, unique=True, verbose_name="DNI")
    email = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono / WhatsApp")

    # Datos de Ubicación
    provincia = models.CharField(max_length=100, default="Catamarca", verbose_name="Provincia")
    localidad = models.CharField(max_length=100, verbose_name="Localidad")

    # Datos del Emprendimiento
    nombre_marca = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nombre del Emprendimiento / Marca")
    rubro = models.ForeignKey(Rubro, on_delete=models.PROTECT, related_name="artesanos", verbose_name="Rubro Principal")
    descripcion_artesanias = models.TextField(verbose_name="Descripción de Productos / Técnicas")

    # Gestión de postulación
    estado_postulacion = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', verbose_name="Estado de Postulación")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Artesano"
        verbose_name_plural = "Artesanos"

    def __str__(self):
        marca = self.nombre_marca if self.nombre_marca else self.nombre_completo
        return f"{marca} ({self.nombre_completo})"