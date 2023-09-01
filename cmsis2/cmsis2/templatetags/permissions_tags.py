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
        return UserCategoryRole.objects.filter(user=user, role__permissions__name=permission).exists()
    except user.DoesNotExist:
        return False


@register.filter(name='has_category_permission')
def has_category_permission(user, category_id, permission_name):
    try:
        user_category_role = UserCategoryRole.objects.get(user=user, category_id=category_id)
        return user_category_role.role.permissions.filter(name=permission_name).exists()
    except UserCategoryRole.DoesNotExist:
        return False
