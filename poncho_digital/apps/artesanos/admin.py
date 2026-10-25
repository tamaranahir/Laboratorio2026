from django.contrib import admin
from django.contrib.auth.models import User
from .models import Artesano, Rubro

@admin.register(Rubro)
class RubroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(Artesano)
class ArtesanoAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'dni', 'email', 'nombre_marca', 'rubro', 'estado_postulacion')
    list_filter = ('estado_postulacion', 'rubro', 'provincia')
    search_fields = ('nombre_completo', 'dni', 'email', 'nombre_marca')

    def save_model(self, request, obj, form, change):
        if obj.estado_postulacion == 'aprobado' and not obj.user:
            # Creamos el usuario en Django
            usuario, creado = User.objects.get_or_create(
                username=obj.dni,
                defaults={
                    'first_name': obj.nombre_completo.split()[0],
                    'email': obj.email
                }
            )
            if creado:
                usuario.set_password('poncho2026')  # Contraseña genérica
                usuario.save()

            # Vinculamos la cuenta creada con el artesano
            obj.user = usuario

        super().save_model(request, obj, form, change)
