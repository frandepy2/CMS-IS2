from django.shortcuts import render, redirect, get_object_or_404

from .models import Usuario
from roles.models import CustomRole, UserCategoryRole
from roles.forms import UserCategoryRoleForm
from django.core.paginator import Paginator, Page

# Create your views here.
def home(request):
    return render(request, 'usuarios/home.html')

def usuarios(request):
    usuario_list = Usuario.objects.all().order_by('id')  # Obtén todos los roles
    paginator = Paginator(usuario_list,5)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'usuarios/usuarios.html', {'page': page})

def manage_user(request, user_id):
    user = Usuario.objects.get(id=user_id)
    user_roles = UserCategoryRole.objects.filter(user=user)
    return render(request, 'usuarios/manage_user.html', {'usuario': user, 'roles':user_roles})

def asignar_rol(request, user_id):
    user = Usuario.objects.get(id=user_id)
    if request.method == 'POST':
        form = UserCategoryRoleForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            return redirect('usuarios')  # Redirige a la vista deseada después de crear el rol
    else:
        form = UserCategoryRoleForm()
        form.fields['user'].initial = user
        form.fields['user'].widget.attrs['disabled'] = True
    return render(request, 'usuarios/asign_user_role.html', {'form': form})
def desasignar_rol(request,role_category_id):
    role_category = get_object_or_404(UserCategoryRole, id=role_category_id)
    role_category.delete()
    return redirect('usuarios')