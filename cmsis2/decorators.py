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


def has_category_permission_decorator(*permission_names):
    """
    Decorador que verifica si un usuario tiene al menos uno de los permisos de categoría especificados.

    :param permission_names: Una lista de nombres de permisos que se deben verificar.
    :type permission_names: str
    :return: La función de vista envuelta si el usuario tiene al menos uno de los permisos de categoría, de lo contrario, retorna una respuesta prohibida.
    :rtype: callable
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, categoria_id, *args, **kwargs):
            user = request.user
            has_permission = False
            for permission_name in permission_names:
                if has_category_permission(user, categoria_id, permission_name):
                    has_permission = True
                    break  # Si se cumple uno de los permisos, no es necesario seguir verificando los demás
            if has_permission:
                return view_func(request, categoria_id, *args, **kwargs)
            else:
                return HttpResponseForbidden("You don't have permission to access this page.")
        return _wrapped_view
    return decorator


def has_some_cat_role_decorator():
    """
    Decorador que verifica si un usuario tiene un rol cualquiera dentro de una categoría.

    :return: La función de vista envuelta si el usuario tiene el permiso de categoría, de lo contrario, retorna una respuesta prohibida.
    :rtype: callable
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, categoria_id, *args, **kwargs):
            user = request.user
            if has_some_category_role(user, categoria_id):
                return view_func(request, categoria_id, *args, **kwargs)
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


def has_some_category_role(user, category_id):
    """
    Verifica si un usuario tiene un rol cualquiera dentro de una categoría.

    :param user: El usuario cuyo permiso de categoría se debe verificar.
    :type user: User (o el tipo de usuario correspondiente en tu modelo de datos)
    :param category_id: El ID de la categoría para la que se debe verificar el rol.
    :type category_id: int
    :return: True si el usuario tiene el rol en la categoría, False en caso contrario.
    :rtype: bool
    """
    try:
        user_category_role = UserCategoryRole.objects.get(user=user, category_id=category_id)
        return user_category_role
    except UserCategoryRole.DoesNotExist:
        return False
