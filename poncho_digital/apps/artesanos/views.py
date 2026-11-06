from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import ArtesanoForm, StandForm, RubroForm, ConsultaForm, RespuestaForm
from .models import Artesano, Stand, Rubro, Consulta
from django.db.models import Count
from django.utils import timezone


# Función auxiliar para controlar acceso exclusivo de Administradores
def es_administrador(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# VISITANTE

# Postulación y consulta de estados
def registro_artesano(request):
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

#Gestion de consultas
# Enviar pregunta a un artesano específico
@login_required
def enviar_consulta(request, artesano_id):

    if request.user.is_authenticated and request.user.is_staff:
        messages.warning(request, "Los administradores no pueden realizar consultas a los artesanos.")
        return redirect('productos:lista')  # o a la vista del catálogo

    artesano = get_object_or_404(Artesano, id=artesano_id)

    if hasattr(request.user, 'artesano') and request.user.artesano == artesano:
        messages.warning(request, "No podés enviarte consultas a vos mismo sobre tu propio producto.")
        return redirect('productos:lista')

    producto_id = request.GET.get('producto_id')
    producto = None

    if producto_id:
        from apps.productos.models import Producto
        producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.usuario = request.user
            consulta.artesano = artesano
            consulta.save()
            messages.success(request, f"¡Tu consulta fue enviada con éxito a {artesano.nombre_completo}!")
            return redirect('artesanos:mis_consultas')
    else:
        initial_data = {}
        if producto:
            initial_data['producto'] = producto
        form = ConsultaForm(initial=initial_data)

    return render(request, 'artesanos/enviar-consulta.html', {
        'form': form,
        'artesano': artesano,
        'producto': producto
    })

# Vista privada del usuario comprador
@login_required
def mis_consultas(request):
    consultas = Consulta.objects.filter(usuario=request.user).select_related('artesano', 'producto')
    return render(request, 'artesanos/mis-consultas.html', {'consultas': consultas})

# Vista privada del Artesano:
@login_required
def consultas_recibidas(request):
    artesano = get_object_or_404(Artesano, user=request.user)
    consultas = Consulta.objects.filter(artesano=artesano).select_related('usuario', 'producto')
    return render(request, 'artesanos/consultas-recibidas.html', {
        'consultas': consultas,
        'artesano': artesano
    })

# Responder consulta
@login_required
def responder_consulta(request, consulta_id):
    artesano = get_object_or_404(Artesano, user=request.user)
    consulta = get_object_or_404(Consulta, id=consulta_id, artesano=artesano)

    if request.method == 'POST':
        form = RespuestaForm(request.POST, instance=consulta)
        if form.is_valid():
            respuesta_obj = form.save(commit=False)
            respuesta_obj.respondido = True
            respuesta_obj.fecha_respuesta = timezone.now()
            respuesta_obj.save()
            messages.success(request, "Respuesta enviada correctamente al cliente.")
            return redirect('artesanos:consultas_recibidas')
    else:
        form = RespuestaForm(instance=consulta)

    return render(request, 'artesanos/responder-consulta.html', {
        'form': form,
        'consulta': consulta
    })

# ADMINISTRADOR
# Evaluación y auditoría de solicitudes
@login_required
@user_passes_test(es_administrador, login_url='index')
def evaluar_solicitudes(request):
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
    artesano = get_object_or_404(Artesano, pk=pk)

    if nuevo_estado in ['aprobado', 'rechazado', 'pendiente']:
        artesano.estado_postulacion = nuevo_estado
        artesano.save()

        if nuevo_estado == 'rechazado' and artesano.user:
            artesano.user.is_active = False
            artesano.user.save()

        if nuevo_estado == 'aprobado':
            messages.success(
                request,
                f"¡Solicitud de '{artesano.nombre_completo}' APROBADA!"
            )
        else:
            messages.success(
                request,
                f"La solicitud de '{artesano.nombre_completo}' pasó a estado: {nuevo_estado.upper()}."
            )
    else:
        messages.error(request, "Estado no válido.")

    return redirect('artesanos:evaluar_solicitudes')

# Gestión y asignación de stands
@login_required
@user_passes_test(es_administrador, login_url='index')
def gestion_stands(request):
    stands = Stand.objects.all().order_by('numero')
    form = StandForm()

    return render(request, 'artesanos/gestion-stands.html', {
        'stands': stands,
        'form': form
    })

@login_required
@user_passes_test(es_administrador, login_url='index')
def editar_stand(request, stand_id):
    stand = get_object_or_404(Stand, id=stand_id)
    stands = Stand.objects.all().order_by('numero')

    if request.method == 'POST':
        form = StandForm(request.POST, instance=stand)
        if form.is_valid():
            stand_editado = form.save(commit=False)
            if stand_editado.artesano:
                stand_editado.estado = 'ocupado'
            else:
                stand_editado.estado = 'disponible'
            stand_editado.save()

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
    stand = get_object_or_404(Stand, id=stand_id)
    numero = stand.numero

    stand.artesano = None
    stand.estado = 'disponible'
    stand.save()

    messages.success(request, f'El Stand N° {numero} fue liberado y volvió a quedar Disponible.')
    return redirect('artesanos:gestion_stands')

# Gestión de rubros
@login_required
def gestion_rubros(request):
    if not request.user.is_staff:
        messages.error(request, 'Acceso denegado. Función reservada para la administración.')
        return redirect('index')

    rubros = Rubro.objects.all()

    if request.method == 'POST':
        form = RubroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Rubro creado con éxito!')
            return redirect('artesanos:gestion_rubros')
    else:
        form = RubroForm()

    return render(request, 'artesanos/gestion_rubros.html', {
        'rubros': rubros,
        'form': form
    })

@login_required
def editar_rubro(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Acceso denegado.')
        return redirect('index')

    rubro = get_object_or_404(Rubro, pk=pk)

    if request.method == 'POST':
        form = RubroForm(request.POST, instance=rubro)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Rubro actualizado con éxito!')
            return redirect('artesanos:gestion_rubros')
    else:
        form = RubroForm(instance=rubro)

    return render(request, 'artesanos/gestion_rubros.html', {
        'form': form,
        'rubro_editar': rubro,
        'rubros': Rubro.objects.all()
    })

@login_required
def eliminar_rubro(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Acceso denegado.')
        return redirect('index')

    rubro = get_object_or_404(Rubro, pk=pk)

    if Artesano.objects.filter(rubro=rubro).exists():
        messages.error(request, f'No se puede eliminar el rubro "{rubro.nombre}" porque tiene artesanos asociados.')
    else:
        rubro.delete()
        messages.success(request, 'Rubro eliminado con éxito.')

    return redirect('artesanos:gestion_rubros')

# Gestion de Reportes
@login_required
@user_passes_test(es_administrador, login_url='index')
def panel_reportes(request):

    # REPORTE 1: Ocupación de Stands
    total_stands = Stand.objects.count()
    stands_ocupados = Stand.objects.filter(artesano__isnull=False).count()
    stands_disponibles = Stand.objects.filter(artesano__isnull=True).count()

    # Porcentaje global de ocupación
    porcentaje_ocupacion = round((stands_ocupados / total_stands * 100), 1) if total_stands > 0 else 0
    # Listado detallado de todos los stands para la tabla
    listado_stands = Stand.objects.all().select_related('artesano').order_by('numero')

    # REPORTE 2: Artesanos registrados agrupados por Rubro
    artesanos_por_rubro = (
        Artesano.objects.filter(estado_postulacion='aprobado')
        .values('rubro__nombre')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # Listado complementario: Productos por Artesano Aprobado
    productos_por_artesano = (
        Artesano.objects.filter(estado_postulacion='aprobado')
        .annotate(total_productos=Count('productos'))
    )

    context = {
        'total_stands': total_stands,
        'stands_ocupados': stands_ocupados,
        'stands_disponibles': stands_disponibles,
        'porcentaje_ocupacion': porcentaje_ocupacion,
        'listado_stands': listado_stands,
        'artesanos_por_rubro': artesanos_por_rubro,
        'productos_por_artesano': productos_por_artesano,
    }

    return render(request, 'artesanos/reportes.html', context)

# ARTESANO - Stand

@login_required
def mi_stand(request):

    artesano = Artesano.objects.filter(user=request.user, estado_postulacion='aprobado').first()

    stand = None
    if artesano:
        stand = Stand.objects.filter(artesano=artesano).first()

    return render(request, 'artesanos/mi-stand.html', {
        'artesano': artesano,
        'stand': stand
    })