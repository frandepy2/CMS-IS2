from django.db import models

LENGUAJE_COMUN_CHOICES = [
    ('MAX_CANT_DENUNCIAS', 'MAX_CANT_DENUNCIAS'),
]

class Parametro(models.Model):
    clave = models.CharField(max_length=20, choices=LENGUAJE_COMUN_CHOICES, unique=True)
    valor = models.CharField(max_length=255)

    def __str__(self):
        return self.clave