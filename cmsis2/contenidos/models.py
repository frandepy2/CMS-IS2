from django.db import models
from django_quill.fields import QuillField
from usuarios.models import Usuario
from categorias.models import Subcategoria


class Plantilla(models.Model):
    descripcion = models.CharField()
    plantilla = QuillField()

    def __str__(self):
        return self.descripcion


class Contenido(models.Model):
    nombre = models.CharField(max_length=100)
    cuerpo = QuillField()
    autor = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_caducidad = models.DateField(null=True, blank= True)
    fecha_publicacion = models.DateTimeField(null=True, blank=True)

    ESTADO_CHOICES = (
        ('BORRADOR', 'Borrador'),
        ('EDICION', 'En Edición'),
        ('REVISION', 'En Revision'),
        ('PUBLICADO', 'Publicado'),
        ('RECHAZADO', 'Rechazado'),
        ('INACTIVO', 'Inactivo'),
    )
    estado = models.CharField(max_length=100, choices=ESTADO_CHOICES)
    cantidad_denuncias = models.IntegerField(null=True, blank=True, default=0)
    cantidad_me_gusta = models.IntegerField(null= True, blank=True, default=0)
    cantidad_compartir = models.IntegerField(null=True, blank=True, default=0)
    cantidad_comentarios = models.IntegerField(null=True, blank=True, default=0)
    cantidad_visualizaciones = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.nombre
