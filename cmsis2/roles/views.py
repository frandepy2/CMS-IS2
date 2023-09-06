from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomRoleForm
from .models import CustomRole, CustomPermission
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from decorators import has_permission_decorator


@login_required
@has_permission_decorator('view_roles')
def roles(request):
    """
    Vista para mostrar la lista de roles y permisos.

    Esta vista muestra una lista paginada de roles y permisos, y requiere que el usuario tenga el permiso 'view_roles' para acceder.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: La página de roles y permisos paginada.
    :rtype: HttpResponse
    """

    page_title = 'Roles y Permisos'
    roles_list = CustomRole.objects.all().order_by('id')  # Obtén todos los roles
    paginator = Paginator(roles_list,5)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'roles/roles.html',
                  {
                      'page_title': page_title,
                      'page': page
                  })


@login_required
@has_permission_decorator('create_roles')
def crear_rol(request):
    """
    Vista para crear un nuevo rol.

    Permite a los usuarios con el permiso 'create_roles' crear un nuevo rol.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: El formulario de creación de roles o la página de roles después de la creación.
    :rtype: HttpResponse
    """

    page_title = 'Crear Nuevo Rol'
    if request.method == 'POST':
        form = CustomRoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('roles')  # Redirige a la vista deseada después de crear el rol
    else:
        form = CustomRoleForm()
    return render(request, 'roles/crear_rol.html',
                  {
                      'page_title': page_title,
                      'form': form
                  })


@login_required
@has_permission_decorator('view_roles')
def mas_informacion_rol(request, role_id):
    """
    Vista para mostrar información detallada de un rol.

    Muestra información detallada de un rol específico y requiere el permiso 'view_roles' para acceder.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :param role_id: El ID del rol que se va a mostrar.
    :type role_id: int
    :return: La página de información detallada del rol.
    :rtype: HttpResponse
    """

    role = CustomRole.objects.get(id=role_id)
    page_title = role.name
    return render(request, 'roles/more_info.html',
                  {
                      'page_title': page_title,
                      'role': role
                  })


@login_required
@has_permission_decorator('edit_roles')
def editar_rol(request,role_id):
    """
    Vista para editar un rol existente.

    Permite a los usuarios con el permiso 'edit_roles' editar un rol existente.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :param role_id: El ID del rol que se va a editar.
    :type role_id: int
    :return: El formulario de edición de roles o la página de roles después de la edición.
    :rtype: HttpResponse
    """

    page_title = 'Modificar Rol'
    role = get_object_or_404(CustomRole, id=role_id)

    # Verifica si es un rol del sistema
    if role.is_system_role:
        # Filtra los permisos para roles del sistema
        permissions = CustomPermission.objects.filter(is_system_permission=True)
    else:
        # Muestra todos los permisos para roles que no son del sistema
        permissions = CustomPermission.objects.all()

    if request.method == 'POST':
        form = CustomRoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('roles')  # Redirige a la lista de roles
    else:
        form = CustomRoleForm(instance=role)

    return render(request, 'roles/editar_rol.html',
                  {
                      'page_title': page_title,
                      'form': form,
                      'role': role
                  })

@login_required
@has_permission_decorator('delete_roles')
def inactivar_rol(request, role_id):
    """
    Vista para activar o desactivar un rol.

    Permite a los usuarios con el permiso 'eliminar_roles' activar o desactivar un rol.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :param role_id: El ID del rol que se va a activar o desactivar.
    :type role_id: int
    :return: Redirige a la lista de roles después de la activación o desactivación.
    :rtype: HttpResponse
    """

    role = get_object_or_404(CustomRole, id=role_id)
    if role.is_active:
        role.is_active = False
    else:
        role.is_active = True
    role.save()
    return redirect('roles')


