from django.db import models
from cmsis2.usuarios.models import Usuario
from cmsis2.interacciones.models import Accion
from cmsis2.contenidos.models import Contenido

# Create your models here.
class Notificacion(models.Model):
    emisor = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True)
    receptor = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True , blank=True)
    accion = models.ForeignKey(Accion, on_delete=models.PROTECT, null=True, blank=True)
    contenido = models.ForeignKey(Contenido, on_delete=models.PROTECT, null=True, blank=True)
    titulo = models.CharField(max_length=255, null=True , blank=True)
    mensaje = models.CharField(max_length=255, null=True,  blank=True)
    leido = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.titulo