# reservas/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reservas.models import Reserva
import re
from .utils import generar_factura_pdf

# Misma información que el array CANCHAS en reservas.html (JS),
# usada aquí solo para calcular tipo de juego y precio total,
# ya que el modelo Reserva no guarda esos datos.
CANCHAS_INFO = {
    'Cancha Principal':          {'tipo': 'Fútbol 5',  'precio': 80000},
    'Cancha Auxiliar':           {'tipo': 'Fútbol 7',  'precio': 95000},
    'Cancha Sintética Norte':    {'tipo': 'Fútbol 5',  'precio': 80000},
    'Cancha Sur':                {'tipo': 'Fútbol 11', 'precio': 120000},
}


def vista_pago(request):
    reserva = Reserva.objects.order_by('-id').first()

    contexto = {'reserva': reserva}

    if reserva:
        info = CANCHAS_INFO.get(reserva.cancha, {})

        # Jugadores según el tipo de cancha (Fútbol 5 -> "5 vs 5", etc.)
        tipo = info.get('tipo', '')
        match_num = re.search(r'\d+', tipo)
        if match_num:
            n = match_num.group(0)
            contexto['jugadores'] = f"{n} vs {n}"
        else:
            contexto['jugadores'] = '—'

        # Total = precio por hora * número de horas (extraído de "duracion", ej. "2 Horas")
        precio_hora = info.get('precio', 0)
        match_horas = re.search(r'\d+', reserva.duracion or '')
        horas = int(match_horas.group(0)) if match_horas else 1
        contexto['total'] = precio_hora * horas
        contexto['duracion_minutos'] = horas * 60

    return render(request, 'pagos/pago.html', contexto)

def descargar_factura(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    pdf_buffer = generar_factura_pdf(reserva_id)
    if pdf_buffer is None:
        return HttpResponse("Reserva no encontrada", status=404)
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{reserva_id}.pdf"'
    return response