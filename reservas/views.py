from django.shortcuts import render

def reservas(request):
    return render(request, 'reservas/reservas.html')

def formulario(request):
    return render(request, 'reservas/formulario.html')