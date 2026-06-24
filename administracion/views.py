from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from usuarios.models import Usuario
from canchas.models import Cancha
from contacto.models import Resena
from reservas.models import Reserva
import json

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