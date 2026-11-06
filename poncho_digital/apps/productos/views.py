from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Producto, Categoria
from .forms import ProductoForm, CategoriaForm
from apps.artesanos.models import Rubro

# VISITANTE

def lista_productos(request):
    categoria_id = request.GET.get('categoria')
    rubro_id = request.GET.get('rubro')

    productos = Producto.objects.filter(activo=True).select_related('artesano', 'categoria')

    if categoria_id and categoria_id.isdigit():
        categoria_id = int(categoria_id)
        productos = productos.filter(categoria_id=categoria_id)
    else:
        categoria_id = None

    if rubro_id and rubro_id.isdigit():
        rubro_id = int(rubro_id)
        productos = productos.filter(artesano__rubro_id=rubro_id)
    else:
        rubro_id = None

    categorias = Categoria.objects.all()
    rubros = Rubro.objects.all()

    return render(request, 'productos/productos.html', {
        'productos': productos,
        'categorias': categorias,
        'rubros': rubros,
        'categoria_seleccionada': categoria_id,
        'rubro_seleccionado': rubro_id,
    })

# ARTESANO

@login_required
def cargar_producto(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Debes iniciar sesión para publicar productos.')
        return redirect('index')

    if not hasattr(request.user, 'artesano') or request.user.artesano.estado_postulacion != 'aprobado':
        messages.error(request, 'Solo los artesanos aprobados pueden publicar productos.')
        return redirect('productos:lista')

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.artesano = request.user.artesano
            producto.activo = True
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
    if not hasattr(request.user, 'artesano'):
        messages.error(request,'Su cuenta no está asociada a ningún perfil de artesano.')
        return redirect('productos:lista')
    producto = get_object_or_404(Producto, pk=pk, artesano=request.user.artesano)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.activo = True
            producto.save()
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
    if not hasattr(request.user, 'artesano'):
        messages.error(request,'Su cuenta no está asociada a ningún perfil de artesano.')
        return redirect('productos:lista')

    producto = get_object_or_404(Producto, pk=pk, artesano=request.user.artesano)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'El producto fue eliminado con éxito.')
    return redirect('productos:mis_productos')

#ADMINISTRADOR
#Gestion Categoria
@login_required
def gestion_categorias(request):

    if not request.user.is_staff:
        messages.error(request, 'Acceso denegado. Función reservada para la administración.')
        return redirect('index')

    categorias = Categoria.objects.all()

    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Categoría creada con éxito!')
            return redirect('productos:gestion_categorias')
    else:
        form = CategoriaForm()

    return render(request, 'productos/gestion_categorias.html', {
        'categorias': categorias,
        'form': form
    })

@login_required
def editar_categoria(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Acceso denegado.')
        return redirect('index')

    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Categoría actualizada!')
            return redirect('productos:gestion_categorias')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'productos/gestion_categorias.html', {
        'form': form,
        'categoria_editar': categoria,
        'categorias': Categoria.objects.all()
    })

@login_required
def eliminar_categoria(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Acceso denegado.')
        return redirect('index')

    categoria = get_object_or_404(Categoria, pk=pk)

    if Producto.objects.filter(categoria=categoria).exists():
        messages.error(request, f'No se puede eliminar "{categoria.nombre}" porque tiene productos asociados.')
    else:
        categoria.delete()
        messages.success(request, 'Categoría eliminada con éxito.')

    return redirect('productos:gestion_categorias')