from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Usuario
from roles.models import CustomRole, UserCategoryRole
from roles.forms import UserSystemRoleFormAg
from django.core.paginator import Paginator, Page
from decorators import has_permission_decorator


@login_required
@has_permission_decorator('view_users')
def usuarios(request):
    """
    Vista para mostrar la lista de usuarios.

    Esta vista muestra una lista paginada de usuarios y requiere que el usuario tenga el permiso 'view_users' para acceder.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: La página de usuarios paginada.
    :rtype: HttpResponse
    """
    page_title = 'Usuarios'
    usuario_list = Usuario.objects.all().order_by('id')  # Obtén todos los roles
    paginator = Paginator(usuario_list,5)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'usuarios/usuarios.html',
                  {
                      'page_title': page_title,
                      'page': page,
                  })
@login_required
@has_permission_decorator('asign_roles')
def manage_user(request, user_id):
    """
    Vista para gestionar un usuario específico.

    Permite a los usuarios con el permiso 'asign_roles' gestionar roles asignados a un usuario en particular.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :param user_id: El ID del usuario que se va a gestionar.
    :type user_id: int
    :return: La página de gestión de usuario.
    :rtype: HttpResponse
    """
    user = Usuario.objects.get(id=user_id)
    user_roles = UserCategoryRole.objects.filter(user=user)
    page_title = user.email
    return render(request, 'usuarios/manage_user.html',
                  {
                      'page_title': page_title,
                      'usuario': user,
                      'roles': user_roles
                  })

@login_required
@has_permission_decorator('asign_roles')
def asignar_rol(request, user_id):
    """
    Vista para asignar un rol a un usuario.

    Permite a los usuarios con el permiso 'asign_roles' asignar un rol a un usuario específico.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :param user_id: El ID del usuario al que se le asignará el rol.
    :type user_id: int
    :return: El formulario de asignación de roles o la página de usuarios después de la asignación.
    :rtype: HttpResponse
    """
    user = Usuario.objects.get(id=user_id)
    page_title = 'Asignar Rol'
    if request.method == 'POST':
        form = UserSystemRoleForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            return redirect('usuarios')  # Redirige a la vista deseada después de crear el rol
    else:
        form = UserSystemRoleForm()
        form.fields['user'].initial = user
        form.fields['user'].widget.attrs['disabled'] = True
    return render(request, 'usuarios/asign_user_role.html',
                  {
                      'page_title': page_title,
                      'form': form
                  })

@login_required
@has_permission_decorator('asign_roles')
def desasignar_rol(request, role_category_id):
    """
    Vista para desasignar un rol de un usuario.

    Permite a los usuarios con el permiso 'asign_roles' desasignar un rol de un usuario.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :param role_category_id: El ID del rol de usuario que se va a desasignar.
    :type role_category_id: int
    :return: Redirige a la lista de usuarios después de la desasignación.
    :rtype: HttpResponse
    """
    role_category = get_object_or_404(UserCategoryRole, id=role_category_id)
    role_category.delete()
    return redirect('usuarios')
