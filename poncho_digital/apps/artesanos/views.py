from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ArtesanoForm, StandForm
from .models import Artesano, Stand



def registro_artesano(request):
    # Si el usuario está logueado, evaluamos si es Admin o Artesano Aprobado
    if request.user.is_authenticated:

        # 1. Caso Administrador
        if request.user.is_staff or request.user.is_superuser:
            return render(request, 'artesanos/registro-artesano.html', {
                'es_admin': True
            })

        # 2. Caso Artesano Aprobado
        artesano = Artesano.objects.filter(user=request.user, estado_postulacion='aprobado').first()
        if artesano:
            return render(request, 'artesanos/registro-artesano.html', {
                'ya_es_artesano': True,
                'artesano': artesano
            })

    # 3. Flujo normal (muestra el formulario a visitantes y usuarios comunes)
    if request.method == 'POST':
        form = ArtesanoForm(request.POST, request.FILES)
        if form.is_valid():
            artesano = form.save(commit=False)
            artesano.estado_postulacion = 'pendiente'
            if request.user.is_authenticated:
                artesano.user = request.user
            artesano.save()
            messages.success(request,
                             '¡Tu solicitud de postulación fue enviada con éxito! El administrador la revisará a la brevedad.')
            return redirect('index')
    else:
        form = ArtesanoForm()

    return render(request, 'artesanos/registro-artesano.html', {'form': form})

def consultar_estado(request):
    artesano = None
    buscado = False
    dni = request.GET.get('dni', '').strip()

    if dni:
        buscado = True
        # Buscamos la postulación asociada a ese DNI
        artesano = Artesano.objects.filter(dni=dni).first()

    return render(request, 'artesanos/consultar-estado.html', {
        'artesano': artesano,
        'buscado': buscado,
        'dni': dni
    })

    #-----------------------------------------------------------
    #ASIGNACION DE STAND
@login_required
def gestion_stands(request):
    # Control de seguridad: si no es administrador (is_staff), rebota la petición
    if not request.user.is_staff:
        messages.error(request, 'Acceso denegado. Esta sección es exclusiva para la administración.')
        return redirect('index')

    stands = Stand.objects.all()

    if request.method == 'POST':
        form = StandForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Stand registrado correctamente!')
            return redirect('artesanos:gestion_stands')
    else:
        form = StandForm()

    return render(request, 'artesanos/gestion-stands.html', {
        'stands': stands,
        'form': form
    })

@login_required
def eliminar_stand(request, stand_id):
    if not request.user.is_staff:
        messages.error(request, 'Acceso denegado.')
        return redirect('index')

    stand = get_object_or_404(Stand, id=stand_id)
    numero = stand.numero
    stand.delete()
    messages.success(request, f'El Stand N° {numero} fue eliminado correctamente.')
    return redirect('artesanos:gestion_stands')

@login_required
def editar_stand(request, stand_id):
    if not request.user.is_staff:
        messages.error(request, 'Acceso denegado.')
        return redirect('index')

    stand = get_object_or_404(Stand, id=stand_id)
    stands = Stand.objects.all()

    if request.method == 'POST':
        # Pasamos instance=stand para que modifique el registro existente
        form = StandForm(request.POST, instance=stand)
        if form.is_valid():
            form.save()
            messages.success(request, f'¡El Stand N° {stand.numero} fue modificado con éxito!')
            return redirect('artesanos:gestion_stands')
    else:
        # Carga el formulario con los datos actuales del stand
        form = StandForm(instance=stand)

    return render(request, 'artesanos/gestion-stands.html', {
        'stands': stands,
        'form': form,
        'stand_editando': stand
    })


@login_required
def mi_stand(request):
    # 1. Buscamos el registro de artesano aprobado del usuario logueado
    artesano = Artesano.objects.filter(user=request.user, estado_postulacion='aprobado').first()

    stand = None
    if artesano:
        # 2. Buscamos el stand asignado a este artesano
        stand = Stand.objects.filter(artesano=artesano).first()

    return render(request, 'artesanos/mi-stand.html', {
        'artesano': artesano,
        'stand': stand
    })