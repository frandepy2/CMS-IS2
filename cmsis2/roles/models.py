from django.db import models
from usuarios.models import Usuario
from categorias.models import Categoria

# Create your models here.
class CustomRole(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    permissions = models.ManyToManyField('CustomPermission', through= 'RolePermission')

    def __str__(self):
        return self.name

class CustomPermission(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class RolePermission(models.Model):
    role = models.ForeignKey(CustomRole, on_delete=models.CASCADE)
    permission = models.ForeignKey(CustomPermission, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.role} - {self.permission}"

class UserCategoryRole(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    category = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(CustomRole, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.category} - {self.role}"
