from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from usuarios.models import Usuario
from canchas.models import Cancha
from contacto.models import Resena
from reservas.models import Reserva
import json


def registro_admin(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'usuarios/registro_admin.html', {'error': 'Las contraseñas no coinciden'})
        if Usuario.objects.filter(email=email).exists():
            return render(request, 'usuarios/registro_admin.html', {'error': 'Este correo ya está registrado'})

        Usuario.objects.create(
            first_name=first_name, last_name=last_name, email=email,
            phone=phone, password=password, rol='ADMIN'
        )
        return redirect('login_admin')

    return render(request, 'usuarios/registro_admin.html')


def login_admin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            usuario = Usuario.objects.get(email=email, password=password)
            if usuario.rol == 'ADMIN':
                return redirect('panel_principal')
            return redirect('inicio')
        except Usuario.DoesNotExist:
            return render(request, 'usuarios/login_admin.html', {'error': 'Correo o contraseña incorrectos'})
    return render(request, 'usuarios/login_admin.html')


def panel_principal(request):
    reservas = Reserva.objects.all().order_by('-id')
    return render(request, 'panel/panel_base.html', {
        'canchas':            Cancha.objects.all(),
        'resenas_activas':    Resena.objects.filter(archivada=False).order_by('-fecha'),
        'resenas_archivadas': Resena.objects.filter(archivada=True).order_by('-fecha'),
        'reservas':           reservas,
        'total_reservas':     reservas.count(),
        'confirmadas':        reservas.filter(estado='Confirmada').count(),
        'pendientes':         reservas.filter(estado='Pendiente').count(),
    })


@require_POST
def aprobar_reserva(request, id):
    try:
        reserva = Reserva.objects.get(id=id)
        reserva.estado = 'Confirmada'
        reserva.save()
        return JsonResponse({'status': 'ok'})
    except Reserva.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)


@require_POST
def eliminar_reserva_admin(request, id):
    try:
        Reserva.objects.get(id=id).delete()
        return JsonResponse({'status': 'ok'})
    except Reserva.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)


def lista_usuarios(request):
    return render(request, 'usuarios/lista_usuarios.html', {
        'usuarios': Usuario.objects.all()
    })


def eliminar_usuario(request, id):
    Usuario.objects.get(id=id).delete()
    return redirect('lista_usuarios')


def editar_usuario(request, id):
    usuario = Usuario.objects.get(id=id)
    if request.method == 'POST':
        usuario.first_name = request.POST.get('first_name')
        usuario.email = request.POST.get('email')
        usuario.phone = request.POST.get('phone')
        usuario.password = request.POST.get('password')
        usuario.save()
        return redirect('lista_usuarios')
    return render(request, 'usuarios/editar_usuarios.html', {'usuario': usuario})
@require_POST
def editar_reserva_admin(request, id):
    try:
        reserva = Reserva.objects.get(id=id)
        data = json.loads(request.body.decode("utf-8"))
        reserva.nombre   = data.get("nombre",   reserva.nombre)
        reserva.correo   = data.get("correo",   reserva.correo)
        reserva.telefono = data.get("telefono", reserva.telefono)
        if data.get("fecha"):
            reserva.fecha = data["fecha"]
        if data.get("hora"):
            reserva.hora  = data["hora"]
        reserva.cancha   = data.get("cancha",   reserva.cancha)
        reserva.duracion = data.get("duracion", reserva.duracion)
        reserva.estado   = data.get("estado",   reserva.estado)
        reserva.save()
        return JsonResponse({'status': 'ok'})
    except Reserva.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'mensaje': str(e)}, status=400)