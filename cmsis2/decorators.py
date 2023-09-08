from functools import wraps
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.urls import reverse
from roles.models import UserCategoryRole


def has_permission_decorator(permission_name):
    """
    Decorador que verifica si un usuario tiene un permiso específico.

    :param permission_name: El nombre del permiso que se debe verificar.
    :type permission_name: str
    :return: La función de vista envuelta si el usuario tiene el permiso, de lo contrario, redirecciona.
    :rtype: callable
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if has_permission(user, permission_name):
                return view_func(request, *args, **kwargs)
            else:
                # Redirige a la página anterior si el usuario no tiene el permiso.
                previous_url = request.META.get('HTTP_REFERER', reverse('home'))
                return HttpResponseRedirect(previous_url)
        return _wrapped_view
    return decorator


def has_category_permission_decorator(category_id, permission_name):
    """
    Decorador que verifica si un usuario tiene un permiso específico de categoría.

    :param category_id: El ID de la categoría para la que se debe verificar el permiso.
    :type category_id: int
    :param permission_name: El nombre del permiso que se debe verificar.
    :type permission_name: str
    :return: La función de vista envuelta si el usuario tiene el permiso de categoría, de lo contrario, retorna una respuesta prohibida.
    :rtype: callable
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if has_category_permission(user, category_id, permission_name):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You don't have permission to access this page.")
        return _wrapped_view
    return decorator


def has_permission(user, permission_name):
    """
    Verifica si un usuario tiene un permiso específico.

    :param user: El usuario cuyo permiso se debe verificar.
    :type user: User (o el tipo de usuario correspondiente en tu modelo de datos)
    :param permission_name: El nombre del permiso que se debe verificar.
    :type permission_name: str
    :return: True si el usuario tiene el permiso, False en caso contrario.
    :rtype: bool
    """
    try:
        return UserCategoryRole.objects.filter(
            user=user,  # Filtra por usuario
            role__is_active=True,  # Filtra por roles activos
            role__permissions__name=permission_name  # Busca el permiso
        ).exists()
    except user.DoesNotExist:
        return False


def has_category_permission(user, category_id, permission_name):
    """
    Verifica si un usuario tiene un permiso específico dentro de una categoría.

    :param user: El usuario cuyo permiso de categoría se debe verificar.
    :type user: User (o el tipo de usuario correspondiente en tu modelo de datos)
    :param category_id: El ID de la categoría para la que se debe verificar el permiso.
    :type category_id: int
    :param permission_name: El nombre del permiso que se debe verificar.
    :type permission_name: str
    :return: True si el usuario tiene el permiso de categoría, False en caso contrario.
    :rtype: bool
    """
    try:
        user_category_role = UserCategoryRole.objects.get(user=user, category_id=category_id)
        return user_category_role.role.permissions.filter(name=permission_name).exists()
    except UserCategoryRole.DoesNotExist:
        return False
