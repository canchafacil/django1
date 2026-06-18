# reservas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... tus otras rutas existentes
    path('pago/', views.vista_pago, name='pago'),
]