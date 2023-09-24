from django.db import models
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.dispatch import receiver
from usuarios.models import Usuario
from categorias.models import Categoria

# Create your models here.
class CustomRole(models.cd):
    """
    Modelo que representa roles personalizados en el sistema.

    :param name: El nombre del rol.
    :type name: str
    :param is_active: Indica si el rol está activo o inactivo.
    :type is_active: bool
    :param is_system_role: Indica si el rol es un rol de sistema.
    :type is_system_role: bool
    :param can_modify: Indica si el rol puede ser modificado.
    :type can_modify: bool
    :param permissions: Los permisos asociados al rol.
    :type permissions: models.ManyToManyField de CustomPermission a través de RolePermission
    """

    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_system_role = models.BooleanField(default=False)
    can_modify = models.BooleanField(default=True)
    permissions = models.ManyToManyField('CustomPermission', through= 'RolePermission')

    def __str__(self):
        return self.name

class CustomPermission(models.Model):
    """
    Modelo que representa permisos personalizados en el sistema.

    :param name: El nombre del permiso.
    :type name: str
    :param description: La descripción del permiso.
    :type description: str
    :param is_system_permission: Indica si el permiso es un permiso de sistema.
    :type is_system_permission: bool
    """

    name = models.CharField(max_length=100)
    description = models.TextField()
    is_system_permission = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class RolePermission(models.Model):
    """
    Modelo que representa la relación entre roles y permisos personalizados.

    :param role: El rol relacionado.
    :type role: CustomRole
    :param permission: El permiso relacionado.
    :type permission: CustomPermission
    """

    role = models.ForeignKey(CustomRole, on_delete=models.CASCADE)
    permission = models.ForeignKey(CustomPermission, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.role} - {self.permission}"

class UserCategoryRole(models.Model):
    """
    Modelo que representa la asignación de roles de categoria a usuarios.

    :param user: El usuario relacionado.
    :type user: Usuario
    :param category: La categoría relacionada (puede ser nula).
    :type category: Categoria
    :param role: El rol relacionado.
    :type role: CustomRole
    """
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    category = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(CustomRole, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.category} - {self.role}"

    class Meta:
        unique_together = ['user', 'category', 'role']

@receiver(post_save, sender=Usuario)
def crear_primer_admin(sender, instance, **kwargs):
    """
    Crea un grupo 'cms_admin' y agrega al usuario a este grupo si es el primer administrador.

    :param sender: El modelo que envía la señal (Usuario en este caso).
    :param instance: La instancia del usuario que fue creada o modificada.
    :param kwargs: Argumentos adicionales de la señal (no se utilizan aquí).
    """
    if Usuario.objects.filter(groups__name='cms_admin').count() == 0:
        print("Asignamos el primer admin")
        admin_group, created = Group.objects.get_or_create(name='cms_admin')
        if created:
            pass
        instance.groups.add(admin_group)
        instance.is_staff = True
        instance.save()

        admin_role = CustomRole.objects.filter(name='Admin').first()
        if admin_role:
            category = None
            user_category_role, created = UserCategoryRole.objects.get_or_create(
                user=instance,
                role=admin_role,
                category=category
            )

            if created:
                print(f"Assigned 'Admin' role to user: {instance}")

            # Assign all admin permissions to the user
            permissions = Permission.objects.all()
            instance.user_permissions.set(permissions)  # Set all admin permissions
        else:
            print("'Admin' role does not exist.")
