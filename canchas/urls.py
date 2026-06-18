from django.urls import path
from . import views

urlpatterns = [
    path('', views.canchas, name='canchas'),
]