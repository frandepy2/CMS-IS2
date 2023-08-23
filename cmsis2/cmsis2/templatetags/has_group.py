from django import template
from django.contrib.auth.models import Group

from usuarios.models import Usuario

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

@register.filter(name='is_subscribed')
def is_subscribed(user_id):
    try:
        user= Usuario.objects.get(id=user_id)
        return user.subscribed
    except Usuario.DoesNotExist:
        return False