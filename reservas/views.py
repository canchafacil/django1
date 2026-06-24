from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import Reserva
def pagina_reservas(request):
    return render(request, "reservas/reservas.html")
def reservas(request):
    todas = Reserva.objects.all().order_by('-id')
    return render(request, "reservas/formulario.html", {"reservas": todas})

@require_POST
def crear_reserva(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        reserva = Reserva.objects.create(
            nombre   = data["nombre"],
            correo   = data["correo"],
            telefono = data["telefono"],
            fecha    = data["fecha"],
            hora     = data["hora"],
            cancha   = data["cancha"],
            duracion = data["duracion"],
        )
        # Guardamos el id en session para que pago.html lo muestre
        request.session["reserva_pendiente_id"] = reserva.id
        return JsonResponse({"status": "ok", "id": reserva.id})
    except (KeyError, json.JSONDecodeError):
        return JsonResponse({"status": "error", "mensaje": "Datos inválidos"}, status=400)

@require_POST
def editar_reserva(request, id):
    try:
        reserva = Reserva.objects.get(id=id)
        data = json.loads(request.body.decode("utf-8"))
        reserva.nombre   = data.get("nombre",   reserva.nombre)
        reserva.correo   = data.get("correo",   reserva.correo)
        reserva.telefono = data.get("telefono", reserva.telefono)
        reserva.fecha    = data.get("fecha",    reserva.fecha)
        reserva.hora     = data.get("hora",     reserva.hora)
        reserva.cancha   = data.get("cancha",   reserva.cancha)
        reserva.duracion = data.get("duracion", reserva.duracion)
        reserva.save()
        return JsonResponse({"status": "ok"})
    except Reserva.DoesNotExist:
        return JsonResponse({"status": "error", "mensaje": "Reserva no encontrada"}, status=404)
    except Exception as e:
        return JsonResponse({"status": "error", "mensaje": str(e)}, status=400)

@require_POST
def eliminar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    reserva.delete()
    return redirect("reservas")

def pago(request):
    reserva_id = request.session.get("reserva_pendiente_id")
    reserva = None
    if reserva_id:
        try:
            reserva = Reserva.objects.get(id=reserva_id)
        except Reserva.DoesNotExist:
            pass
    return render(request, "paginas/pago.html", {"reserva": reserva})