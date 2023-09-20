from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from usuarios.models import Usuario
from categorias.models import Subcategoria

# Create your models here.
class Contenido(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    cuerpo = RichTextUploadingField()
    estado = models.CharField(max_length=100)
    autor = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.PROTECT, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_caducidad = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nombre