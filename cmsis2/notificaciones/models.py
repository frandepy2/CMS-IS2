from django.db import models
from usuarios.models import Usuario
from interacciones.models import Accion
from contenidos.models import Contenido

# Create your models here.
class Notificacion(models.Model):
    emisor = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='emisor', null=True, blank=True)
    receptor = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='receptor', null=True , blank=True)
    accion = models.ForeignKey(Accion, on_delete=models.PROTECT, null=True, blank=True)
    contenido = models.ForeignKey(Contenido, on_delete=models.PROTECT, null=True, blank=True)
    titulo = models.CharField(max_length=255, null=True , blank=True)
    mensaje = models.CharField(max_length=255, null=True,  blank=True)
    fecha = models.DateTimeField(auto_now=True)
    leido = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.titulo