from django.db import models

# Create your models here.
class Parametro(models.Model):
    clave = models.CharField(max_length=100)
    valor = models.CharField(max_length=255)

    def __str__(self):
        return self.clave

