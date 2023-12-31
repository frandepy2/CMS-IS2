from django.db import models
from usuarios.models import Usuario
from interacciones.models import Accion
from contenidos.models import Contenido

# Create your models here.
class Notificacion(models.Model):
    """
    Modelo que representa una notificación en el sistema.

    Cada notificación tiene un emisor, un receptor, una acción (opcional), un contenido (opcional),
    un título, un mensaje, una fecha de creación, y un estado de leído.

    :ivar emisor: El usuario que emite la notificación.
    :ivar receptor: El usuario que recibe la notificación.
    :ivar accion: La acción asociada con la notificación (opcional).
    :ivar contenido: El contenido asociado con la notificación (opcional).
    :ivar titulo: El título de la notificación.
    :ivar mensaje: El mensaje de la notificación.
    :ivar fecha: La fecha y hora de creación de la notificación.
    :ivar leido: Indica si la notificación ha sido marcada como leída.
    """
    emisor = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='emisor', null=True, blank=True)
    receptor = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='receptor', null=True , blank=True)
    accion = models.ForeignKey(Accion, on_delete=models.PROTECT, null=True, blank=True)
    contenido = models.ForeignKey(Contenido, on_delete=models.PROTECT, null=True, blank=True)
    titulo = models.CharField(max_length=255, null=True , blank=True)
    mensaje = models.CharField(max_length=255, null=True,  blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.titulo