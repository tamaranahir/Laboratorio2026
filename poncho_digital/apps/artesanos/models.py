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

# 2. Postulación y Perfil del Artesano
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

# 3. Asignación y Puestos de Stand
class Stand(models.Model):
    PABELLON_CHOICES = [
        ('pabellon_artesanias_1', 'Pabellón de Artesanías 1'),
        ('pabellon_artesanias_2', 'Pabellón de Artesanías 2'),
        ('pabellon_turismo', 'Pabellón de Turismo'),
        ('poncho_diseno', 'Poncho Diseño'),
        ('mercado_cultural', 'Mercado Cultural'),
        ('sector_gastronomico', 'Sector Gastronómico / Foodtrucks'),
        ('sector_comercial', 'Sector Comercial'),
    ]

    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('ocupado', 'Ocupado'),
        ('mantenimiento', 'En Mantenimiento'),
    ]

    numero = models.IntegerField(unique=True, verbose_name="Número de Stand")

    ubicacion = models.CharField(
        max_length=50,
        choices=PABELLON_CHOICES,
        default='pabellon_artesanos',
        verbose_name="Pabellón / Sector"
    )

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible', verbose_name="Estado")
    artesano = models.ForeignKey(
        Artesano,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stands',
        verbose_name="Artesano Asignado"
    )

    class Meta:
        verbose_name = "Stand"
        verbose_name_plural = "Stands"

    def save(self, *args, **kwargs):
        # Si se asignó un artesano, el estado pasa automáticamente a 'ocupado'
        if self.artesano:
            self.estado = 'ocupado'
        # Si se quita el artesano y no está en mantenimiento, vuelve a 'disponible'
        elif self.estado == 'ocupado' and not self.artesano:
            self.estado = 'disponible'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Stand N° {self.numero} - {self.ubicacion} ({self.get_estado_display()})"

#️🚨 VALE AGREGA ESTO AL FINAL- MODELO PARA LAS CONSULTAS#

class Consulta(models.Model):
    ASUNTOS = [
        ('precio', 'Consulta sobre Precios / Presupuesto'),
        ('producto', 'Detalles o Medidas del Producto'),
        ('envio', 'Envíos o Retiro en Feria / Stand'),
        ('personalizado', 'Pedido Personalizado / Encargo'),
        ('otro', 'Otro motivo'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultas_realizadas')
    artesano = models.ForeignKey('Artesano', on_delete=models.CASCADE, related_name='consultas_recibidas')
    producto = models.ForeignKey('productos.Producto', on_delete=models.SET_NULL, null=True, blank=True, related_name='consultas')

    asunto = models.CharField(max_length=50, choices=ASUNTOS, default='producto')
    mensaje = models.TextField(verbose_name="Pregunta o Mensaje")

    respuesta = models.TextField(blank=True, null=True, verbose_name="Respuesta del Artesano")
    respondido = models.BooleanField(default=False)

    fecha_envio = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-fecha_envio']
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"

    def __str__(self):
        return f"Consulta de {self.usuario.username} a {self.artesano.nombre_completo} ({self.get_asunto_display()})"