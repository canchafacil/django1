# reservas/views.py
from django.shortcuts import render

def vista_pago(request):
    return render(request, 'pagos/pago.html') # Asegúrate de que este archivo exista en templates