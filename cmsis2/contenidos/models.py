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
    estado = models.CharField(max_length=100)
    autor = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.PROTECT, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_caducidad = models.DateField(null=True, blank= True)

    def __str__(self):
        return self.nombre
