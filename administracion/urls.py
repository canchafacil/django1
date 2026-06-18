from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicioadmi, name='inicioadmi'),
    path('panel/', views.panel_control, name='admin_panel'),
]