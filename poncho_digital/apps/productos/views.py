from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Producto, Categoria
from .forms import ProductoForm

def lista_productos(request):
    categoria_id = request.GET.get('categoria')
    productos = Producto.objects.filter(activo=True).select_related('artesano', 'categoria')

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    categorias = Categoria.objects.all()

    context = {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': int(categoria_id) if categoria_id and categoria_id.isdigit() else None
    }
    return render(request, 'productos/productos.html', context)


@login_required
def cargar_producto(request):
    # 1. Si no está logueado
    if not request.user.is_authenticated:
        messages.warning(request, 'Debes iniciar sesión para publicar productos.')
        return redirect('index')

    # 2. Verificar de forma segura si el usuario es un Artesano Aprobado (evita que el Admin rompa la vista)
    if not hasattr(request.user, 'artesano') or request.user.artesano.estado_postulacion != 'aprobado':
        messages.error(request, 'Solo los artesanos aprobados pueden publicar productos.')
        return redirect('productos:lista')  # Redirige suavemente al catálogo

    # 3. Flujo normal de carga de producto para el artesano
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.artesano = request.user.artesano
            producto.save()
            messages.success(request, '¡Producto publicado con éxito!')
            return redirect('productos:mis_productos')
    else:
        form = ProductoForm()

    return render(request, 'productos/cargar_producto.html', {'form': form})

@login_required
def mis_productos(request):
    if not hasattr(request.user, 'artesano'):
        messages.error(request, 'Su cuenta de usuario no está asociada a ningún perfil de artesano.')
        return redirect('productos:lista')

    productos = Producto.objects.filter(artesano=request.user.artesano)
    return render(request, 'productos/mis_productos.html', {'productos': productos})

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, artesano=request.user.artesano)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto actualizado correctamente!')
            return redirect('productos:mis_productos')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'productos/cargar_producto.html', {
        'form': form,
        'es_edicion': True,
        'producto': producto
    })

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, artesano=request.user.artesano)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'El producto fue eliminado con éxito.')
    return redirect('productos:mis_productos')