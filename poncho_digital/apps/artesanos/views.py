from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ArtesanoForm, StandForm
from .models import Artesano, Stand

# Función auxiliar para controlar acceso exclusivo de Administradores
def es_administrador(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# 1. Postulación y consulta de estados

def registro_artesano(request):
    """Permite a los postulantes enviar su formulario de inscripción."""
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return render(request, 'artesanos/registro-artesano.html', {'es_admin': True})

        artesano = Artesano.objects.filter(user=request.user, estado_postulacion='aprobado').first()
        if artesano:
            return render(request, 'artesanos/registro-artesano.html', {'ya_es_artesano': True, 'artesano': artesano})

    if request.method == 'POST':
        form = ArtesanoForm(request.POST, request.FILES)
        fotos = request.FILES.getlist('foto_producto')

        # Validación de fotografías en el servidor
        if not fotos or len(fotos) == 0:
            messages.error(request, 'Es obligatorio adjuntar al menos una fotografía de sus productos artesanales.')
        elif form.is_valid():
            artesano = form.save(commit=False)
            artesano.estado_postulacion = 'pendiente'
            if request.user.is_authenticated:
                artesano.user = request.user
            artesano.save()
            messages.success(request,
                             '¡Tu solicitud de postulación fue enviada con éxito! La administración la evaluará a la brevedad.')
            return redirect('index')
        else:
            messages.error(request, 'Por favor corrija los errores marcados en el formulario.')
    else:
        form = ArtesanoForm()

    return render(request, 'artesanos/registro-artesano.html', {'form': form})

def consultar_estado(request):
    """Permite a un postulante consultar el estado de su trámite ingresando su DNI."""
    artesano = None
    buscado = False
    dni = request.GET.get('dni', '').strip()

    if dni:
        buscado = True
        if not dni.isdigit() or len(dni) != 8:
            messages.error(request, "Por favor, ingrese un número de DNI válido de 8 dígitos numéricos.")
        else:
            artesano = Artesano.objects.filter(dni=dni).first()

    return render(request, 'artesanos/consultar-estado.html', {
        'artesano': artesano,
        'buscado': buscado,
        'dni': dni
    })

# 2. Evaluación y auditoría de solicitudes
@login_required
@user_passes_test(es_administrador, login_url='index')
def evaluar_solicitudes(request):
    """Panel centralizado para que el Administrador revise las solicitudes recibidas.Permite filtrar por estado (pendiente, aprobado, rechazado, todos)."""
    estado_filtro = request.GET.get('estado', 'pendiente')

    if estado_filtro == 'todos':
        solicitudes = Artesano.objects.all().order_by('-fecha_registro')
    else:
        solicitudes = Artesano.objects.filter(estado_postulacion=estado_filtro).order_by('-fecha_registro')

    context = {
        'solicitudes': solicitudes,
        'estado_actual': estado_filtro,
    }
    return render(request, 'artesanos/evaluar-solicitudes.html', context)

@login_required
@user_passes_test(es_administrador, login_url='index')
def cambiar_estado_solicitud(request, pk, nuevo_estado):
    """
    Dictamina la solicitud.
    - Al aprobar: crea/activa la cuenta de User.
    - Al rechazar o pasar a pendiente: desactiva la cuenta (is_active = False) para bloquear el login.
    """
    artesano = get_object_or_404(Artesano, pk=pk)

    if nuevo_estado in ['aprobado', 'rechazado', 'pendiente']:
        artesano.estado_postulacion = nuevo_estado

        if nuevo_estado == 'aprobado':
            username_base = str(artesano.dni)
            clave_generica = "poncho2026"

            # 1. Buscamos o creamos el usuario de Django
            user_artesano, created = User.objects.get_or_create(
                username=username_base,
                defaults={'email': artesano.email}
            )

            # 2. Asignamos clave y activamos el usuario
            user_artesano.set_password(clave_generica)
            user_artesano.is_active = True  # Permite el acceso
            user_artesano.save()

            # 3. Vinculamos al artesano
            artesano.user = user_artesano
            artesano.save()

            messages.success(
                request,
                f"¡Solicitud de '{artesano.nombre_completo}' APROBADA! "
                f"Credenciales -> Usuario: {username_base} | Contraseña: {clave_generica}"
            )
        else:
            # Si pasa a RECHAZADO o PENDIENTE, desactivamos el acceso al sistema
            if artesano.user:
                artesano.user.is_active = False  # Bloquea el login en Django
                artesano.user.save()

            artesano.save()
            messages.success(
                request,
                f"La solicitud de '{artesano.nombre_completo}' pasó a estado: {nuevo_estado.upper()}."
            )
    else:
        messages.error(request, "Estado no válido.")

    return redirect('artesanos:evaluar_solicitudes')

#  3. Gestión y asignación de stands
@login_required
@user_passes_test(es_administrador, login_url='index')
def gestion_stands(request):
    """
    Panel para que la administración consulte, ordene y registre nuevos puestos/pabellones.
    """
    # Ordenamos prolijamente por ubicación (pabellón) y número de stand
    stands = Stand.objects.all().order_by('ubicacion', 'numero')

    if request.method == 'POST':
        form = StandForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Stand registrado / asignado correctamente!')
            return redirect('artesanos:gestion_stands')
        else:
            messages.error(request, 'Ocurrió un error al intentar registrar el stand. Revisa los datos.')
    else:
        form = StandForm()

    return render(request, 'artesanos/gestion-stands.html', {
        'stands': stands,
        'form': form
    })


@login_required
@user_passes_test(es_administrador, login_url='index')
def editar_stand(request, stand_id):
    """
    Permite modificar la ubicación o reasignar un stand existente.
    """
    stand = get_object_or_404(Stand, id=stand_id)
    stands = Stand.objects.all().order_by('ubicacion', 'numero')

    if request.method == 'POST':
        form = StandForm(request.POST, instance=stand)
        if form.is_valid():
            form.save()
            messages.success(request, f'¡El Stand N° {stand.numero} fue actualizado con éxito!')
            return redirect('artesanos:gestion_stands')
        else:
            messages.error(request, 'Ocurrió un error al intentar actualizar el stand. Revisa los datos.')
    else:
        form = StandForm(instance=stand)

    return render(request, 'artesanos/gestion-stands.html', {
        'stands': stands,
        'form': form,
        'stand_editando': stand
    })


@login_required
@user_passes_test(es_administrador, login_url='index')
def eliminar_stand(request, stand_id):
    """
    En lugar de borrar el puesto de la base de datos, desasigna al artesano y lo deja 'disponible'.
    """
    stand = get_object_or_404(Stand, id=stand_id)
    numero = stand.numero

    stand.artesano = None
    stand.estado = 'disponible'
    stand.save()

    messages.success(request, f'El Stand N° {numero} fue liberado y volvió a quedar Disponible.')
    return redirect('artesanos:gestion_stands')


@login_required
def mi_stand(request):
    """
    Vista privada del Artesano para consultar su puesto asignado en la feria.
    """
    artesano = Artesano.objects.filter(user=request.user, estado_postulacion='aprobado').first()

    stand = None
    if artesano:
        stand = Stand.objects.filter(artesano=artesano).first()

    return render(request, 'artesanos/mi-stand.html', {
        'artesano': artesano,
        'stand': stand
    })