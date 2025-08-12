from django.db import models
from oficina.models import Oficina


class Persona(models.Model):
        nombre = models.CharField(max_length=100)
        apellido = models.CharField(max_length=100)
        oficina = models.ForeignKey(Oficina, on_delete=models.CASCADE)
        edad = models.IntegerField()

        class Meta:
            
            ordering = ['apellido', 'nombre']

        def __str__(self):
            return f"{self.nombre} {self.apellido} ({self.oficina.nombre})"

# Create your models here.
