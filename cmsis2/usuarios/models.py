from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .manager import CustomUserManager


# Create your models here.
class Usuario(AbstractUser):
    """
    Extiende el modelo AbstractUser para representar usuarios personalizados.

    Este modelo agrega el campo `subscribed` para indicar si un usuario está suscrito.
    """
    username = models.CharField(max_length=255, unique= True)
    email = models.CharField(max_length=255,unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    subscribed = models.BooleanField(default=True)

    objects = CustomUserManager()
    def __str__(self):
        return self.email

@receiver(post_save, sender=Usuario)
def crear_primer_admin(sender, instance, **kwargs):
    """
    Crea un grupo 'cms_admin' y agrega al usuario a este grupo si es el primer administrador.

    :param sender: El modelo que envía la señal (Usuario en este caso).
    :param instance: La instancia del usuario que fue creada o modificada.
    :param kwargs: Argumentos adicionales de la señal (no se utilizan aquí).
    """
    if Usuario.objects.filter(groups__name='cms_admin').count() == 0:
        admin_group, created = Group.objects.get_or_create(name='cms_admin')
        if created:
            pass

        instance.groups.add(admin_group)