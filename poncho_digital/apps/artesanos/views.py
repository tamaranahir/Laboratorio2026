from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ArtesanoForm
from .models import Artesano

def registro_artesano(request):
    if request.method == 'POST':
        form = ArtesanoForm(request.POST, request.FILES)
        if form.is_valid():
            artesano = form.save(commit=False)
            artesano.estado_postulacion = 'pendiente'  # Se guarda en estado Pendiente
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