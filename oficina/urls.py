from django.urls import path
from . import views

urlpatterns = [
    path('oficinas/', views.oficina_list, name='oficina_list'),
    path('oficinas/nueva/', views.oficina_create, name='oficina_create'),

]

