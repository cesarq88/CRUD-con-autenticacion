from django.db import models

    # Create your models here.


class Oficina (models.Model):
        nombre = models.CharField(max_length=100)
        nombre_corto = models.CharField(max_length=255)


        def __str__(self):
            return self.nombre
        

    