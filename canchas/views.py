from django.shortcuts import render
from . import views

def canchas(request):
    return render(request, 'canchas/canchas.html')
