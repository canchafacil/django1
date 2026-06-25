from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.cancha_admin,
        name='cancha_admin'
    ),

    path(
        'agregar/',
        views.agregar_cancha,
        name='agregar_cancha'
    ),

    path(
        'editar/<int:id>/',
        views.editar_cancha,
        name='editar_cancha'
    ),

    path(
        'eliminar/<int:id>/',
        views.eliminar_cancha,
        name='eliminar_cancha'
    ),
]