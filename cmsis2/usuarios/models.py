from django.contrib.auth.models import AbstractUser, Group
from django.db import models
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