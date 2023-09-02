# yourapp/decorators.py

from functools import wraps
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.urls import reverse
from roles.models import UserCategoryRole


def has_permission_decorator(permission_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if has_permission(user, permission_name):
                return view_func(request, *args, **kwargs)
            else:
                # Redirect to the previous page
                previous_url = request.META.get('HTTP_REFERER', reverse('home'))
                return HttpResponseRedirect(previous_url)
        return _wrapped_view
    return decorator


def has_category_permission_decorator(category_id, permission_name):
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
    try:
        return UserCategoryRole.objects.filter(user=user, role__permissions__name=permission_name).exists()
    except user.DoesNotExist:
        return False


def has_category_permission(user, category_id, permission_name):
    try:
        user_category_role = UserCategoryRole.objects.get(user=user, category_id=category_id)
        return user_category_role.role.permissions.filter(name=permission_name).exists()
    except UserCategoryRole.DoesNotExist:
        return False
