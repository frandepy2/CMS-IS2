from django import template
from django.contrib.auth.models import Group

from usuarios.models import Usuario

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Comprueba si el usuario pertenece a un grupo específico.

    :param user: El usuario que se va a comprobar.
    :param group_name: El nombre del grupo a verificar.
    :return: True si el usuario pertenece al grupo, False si no.
    """
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

@register.filter(name='is_subscribed')
def is_subscribed(user_id):
    """
    Comprueba si un usuario está suscrito.

    :param user_id: El ID del usuario a comprobar.
    :return: True si el usuario está suscrito, False si no o si el usuario no existe.
    """
    try:
        user= Usuario.objects.get(id=user_id)
        return user.subscribed
    except Usuario.DoesNotExist:
        return False