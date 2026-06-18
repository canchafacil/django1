from django.urls import path
from . import views

urlpatterns = [
    path('', views.contacto, name='contacto'),
    path('nosotros/', views.nosotros, name='nosotros'),
]