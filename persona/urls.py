from django.urls import path
from . import views


app_name = 'persona'

urlpatterns = [
    path('personas/', views.persona_list, name='persona_list'),
    path('personas/nueva/', views.persona_create, name='persona_create'),
    path('personas/<int:pk>/editar/', views.persona_update, name='persona_update'),
    path('personas/<int:pk>/eliminar/', views.persona_delete, name='persona_delete'),
    path('personas/<int:pk>/', views.persona_detail, name='persona_detail'), 
    path('personas/importar/', views.persona_importar, name='persona_importar'),


]
