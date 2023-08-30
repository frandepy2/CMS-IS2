from django import template

from usuarios.models import Usuario
from roles.models import CustomRole, UserCategoryRole

register = template.Library()


@register.filter(name='has_permission')
def has_permission(user, permission):
    try:
        #user_obj = Usuario.objects.get(id=user.id)
        #return user_obj.has_perm(permission)

        return UserCategoryRole.objects.filter(user=user, role__permissions__name=permission).exists()
    except user.DoesNotExist:
        return False
