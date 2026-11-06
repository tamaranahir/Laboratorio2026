from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.artesanos.models import Artesano
from .forms import RegistroClienteForm

# ARTESANO Y CUENTA

def iniciar_sesion(request):
    if request.method == 'POST':
        username_ingresado = request.POST.get('username')
        clave_ingresada = request.POST.get('password')

        user = authenticate(request, username=username_ingresado, password=clave_ingresada)

        if user is not None:

            if not user.is_active:
                messages.error(request, 'Esta cuenta ha sido deshabilitada.')
                return render(request, 'usuario/login.html')

            if not user.is_superuser:
                artesano_check = Artesano.objects.filter(dni=user.username).first()
                if artesano_check and artesano_check.estado_postulacion == 'rechazado':
                    messages.error(request, 'Tu solicitud fue rechazada. No tienes acceso al sistema.')
                    return render(request, 'usuario/login.html')

            login(request, user)

            artesano = Artesano.objects.filter(dni=user.username, estado_postulacion='aprobado').first()
            if artesano and not artesano.user:
                artesano.user = user
                artesano.save()
            return redirect('index')
        else:
            messages.error(request, 'DNI o contraseña incorrectos.')

    return render(request, 'usuario/login.html')


def salir(request):
    logout(request)
    return redirect('usuario:login')

# CLIENTE Y BD

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Cuenta creada con éxito! Ya podés iniciar sesión como cliente.")
            return redirect('usuario:login')
    else:
        form = RegistroClienteForm()

    return render(request, 'usuario/registro.html', {'form': form})
