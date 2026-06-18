from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservas, name='reservas'),
    path('formulario/', views.formulario, name='formulario'),
]
