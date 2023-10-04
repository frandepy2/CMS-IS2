from django import template
from roles.models import UserCategoryRole

register = template.Library()


@register.filter(name='has_permission')
def has_permission(user, permission):
    """
        Comprueba si un usuario tiene un permiso específico.

        Args:
            user (Usuario): El usuario cuyos permisos se verificarán.
            permission (str): El nombre del permiso que se desea verificar.

        Returns:
            bool: True si el usuario tiene el permiso, False en caso contrario.
        """
    try:
        return UserCategoryRole.objects.filter(
            user=user,  # Filtra por usuario
            role__is_active=True,  # Filtra por roles activos
            role__permissions__name=permission  # Filtra por nombre de permisos
        ).exists()
    except user.DoesNotExist:
        return False


@register.filter(name='has_role')
def has_role(user, role_name):
    return UserCategoryRole.objects.filter(user=user, role__name=role_name).exists()


@register.simple_tag(name='has_category_permission')
def has_category_permission(user, category_id, permission_name):
    try:
        user_category_role = UserCategoryRole.objects.get(user=user, category_id=category_id)
        return user_category_role.role.permissions.filter(name=permission_name).exists()
    except UserCategoryRole.DoesNotExist:
        return False


@register.filter(name='has_category_role')
def has_category_role(user, category_id):
    try:
        user_category_role = UserCategoryRole.objects.get(user=user, category_id=category_id)
        return user_category_role
    except UserCategoryRole.DoesNotExist:
        return False
