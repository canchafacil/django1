from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('inicioadmi/', views.inicioadmi, name='inicioadmi'),
    
]