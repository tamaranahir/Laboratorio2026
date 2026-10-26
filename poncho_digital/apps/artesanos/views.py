from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ArtesanoForm
from .models import Artesano


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