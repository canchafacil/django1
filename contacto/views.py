from django.shortcuts import render

def contacto(request):
    return render(request, 'contacto/contacto.html')

def nosotros(request):
    return render(request, 'contacto/nosotros.html')