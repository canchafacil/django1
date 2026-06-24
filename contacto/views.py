from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import Resena


def nosotros(request):
    if request.method == 'POST':
        nombre    = request.POST.get('nombre', '').strip()
        jugador   = request.POST.get('jugador', '').strip()
        cancha    = request.POST.get('cancha', '').strip()
        estrellas = int(request.POST.get('estrellas', 0))
        texto     = request.POST.get('texto', '').strip()
        if nombre and texto:
            Resena.objects.create(nombre=nombre, jugador=jugador, cancha=cancha, estrellas=estrellas, texto=texto)
        return redirect('nosotros')

    resenas = Resena.objects.filter(archivada=False).order_by('-fecha')
    total = resenas.count()
    promedio = round(sum(r.estrellas for r in resenas) / total, 1) if total else '—'
    return render(request, 'contacto/nosotros.html', {'resenas': resenas, 'promedio': promedio})


def contacto(request):  # ✅ vista propia para contacto
    return render(request, 'contacto/contacto.html')


@require_POST
def resena_archivar(request, id):
    resena = get_object_or_404(Resena, id=id)
    resena.archivada = True
    resena.save()
    return JsonResponse({'ok': True})


@require_POST
def resena_restaurar(request, id):
    resena = get_object_or_404(Resena, id=id)
    resena.archivada = False
    resena.save()
    return JsonResponse({'ok': True})


@require_POST
def resena_eliminar(request, id):
    resena = get_object_or_404(Resena, id=id)
    resena.delete()
    return JsonResponse({'ok': True})


@require_POST
def resena_editar(request, id):
    resena = get_object_or_404(Resena, id=id)
    try:
        data = json.loads(request.body)
        resena.texto = data.get('texto', resena.texto)
        resena.save()
        return JsonResponse({'ok': True})
    except Exception:
        return JsonResponse({'ok': False}, status=400)