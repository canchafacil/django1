from django.shortcuts import render

# Esta es la vista para el login del administrador
def inicioadmi(request):
    return render(request, 'administracion/inicioadmi.html')

# Esta es la vista para el panel de control después de loguearse
def panel_control(request):
    return render(request, 'administracion/admi.html')