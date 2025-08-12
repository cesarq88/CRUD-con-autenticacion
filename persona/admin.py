from django.contrib import admin
from .models import Persona

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('apellido','nombre','edad','oficina')

# Register your models here.
