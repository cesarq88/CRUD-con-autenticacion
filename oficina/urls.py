from django.urls import path
from . import views

urlpatterns = [
    path('oficinas/', views.oficina_list, name='oficina_list'),
    path('oficinas/nueva/', views.oficina_create, name='oficina_create'),
    path('oficinas/<int:pk>/editar/', views.oficina_update, name='oficina_update'),
    path('oficinas/<int:pk>/eliminar/', views.oficina_delete, name='oficina_delete'),
    path('oficinas/<int:pk>/', views.oficina_detail, name='oficina_detail'),
    path('oficinas/importar/', views.oficina_importar, name='oficina_importar'),
]

