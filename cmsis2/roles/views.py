from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomRoleForm
from .models import CustomRole
from django.core.paginator import Paginator, Page

# Create your views here.
def roles(request):
    roles_list = CustomRole.objects.all().order_by('id')  # Obtén todos los roles
    paginator = Paginator(roles_list,5)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'roles/roles.html', {'page': page})

def crear_rol(request):
    if request.method == 'POST':
        form = CustomRoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('roles')  # Redirige a la vista deseada después de crear el rol
    else:
        form = CustomRoleForm()
    return render(request, 'roles/crear_rol.html', {'form': form})

def mas_informacion_rol(request, role_id):
    role = CustomRole.objects.get(id=role_id)
    return render(request, 'roles/more_info.html', {'role': role})

def editar_rol(request,role_id):
    role = get_object_or_404(CustomRole, id=role_id)

    if request.method == 'POST':
        form = CustomRoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('roles')  # Redirect to the list of roles
    else:
        form = CustomRoleForm(instance=role)

    return render(request, 'roles/editar_rol.html', {'form': form, 'role': role})

def inactivar_rol(request,role_id):
    role = get_object_or_404(CustomRole, id=role_id)
    if role.is_active :
        role.is_active = False
    else:
        role.is_active = True
    role.save()
    return redirect('roles')

