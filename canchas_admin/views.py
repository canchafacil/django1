from django.shortcuts import render, redirect, get_object_or_404
from .models import Cancha
from .forms import CanchaForm


def cancha_admin(request):

    canchas = Cancha.objects.all()

    return render(request,
                  'canchas/cancha_admin.html',
                  {'canchas': canchas})


def agregar_cancha(request):

    if request.method == 'POST':

        form = CanchaForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()

    return redirect('cancha_admin')


def editar_cancha(request, id):

    cancha = get_object_or_404(
        Cancha,
        id=id
    )

    if request.method == 'POST':

        form = CanchaForm(
            request.POST,
            request.FILES,
            instance=cancha
        )

        if form.is_valid():
            form.save()

            return redirect('cancha_admin')

    form = CanchaForm(
        instance=cancha
    )

    return render(
        request,
        'canchas/editar.html',
        {'form': form}
    )


def eliminar_cancha(request, id):

    cancha = get_object_or_404(
        Cancha,
        id=id
    )

    cancha.delete()

    return redirect('cancha_admin')