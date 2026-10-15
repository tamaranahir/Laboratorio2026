from django.db import models

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
    artesano = models.OneToOneField( 'Artesano', on_delete=models.SET_NULL, null=True, blank=True, related_name='stand' )

    class Meta: verbose_name = "Stand"
    verbose_name_plural = "Stands"

    def __str__(self):
        estado = f"Ocupado por {self.artesano.nombre_marca}" if self.artesano else "Disponible"
        return f"Stand {self.numero} - {self.pabellon} ({estado})"


# 3. Postulación y Perfil del Artesano
class Artesano(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente de Evaluación'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    )

    # Datos Personales
    nombre_completo = models.CharField(max_length=100, verbose_name="Apellido y Nombre")
    dni = models.CharField(max_length=8, unique=True, verbose_name="DNI")
    email = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")

    # Datos de Procedencia
    provincia = models.CharField(max_length=50, default='Catamarca')
    departamento = models.CharField(max_length=50, blank=True)

    # Datos del Emprendimiento
    nombre_marca = models.CharField(max_length=100, verbose_name="Nombre del Emprendimiento o Marca")
    descripcion_tecnicas = models.TextField(verbose_name="Descripción de Técnicas")

    # Asociaciones
    rubro = models.ForeignKey('Rubro', on_delete=models.PROTECT, related_name="artesanos", verbose_name="Rubro")

    # Gestión de postulación
    estado_postulacion = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Artesano"
        verbose_name_plural = "Artesanos"

        def __str__(self):
            return f"{self.nombre_marca} ({self.nombre_completo})"

