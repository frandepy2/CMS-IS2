from django.db import models
from usuarios.models import Usuario
from contenidos.models import Contenido

# Create your models here.
class Comentario(models.Model):
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.autor.username} en "{self.contenido.nombre}"'

class Accion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE,null=True, blank=True)
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE, related_name='acciones')
    tipo_accion = models.CharField(max_length=10)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Accion en "{self.contenido.nombre}" accion : {self.tipo_accion}'