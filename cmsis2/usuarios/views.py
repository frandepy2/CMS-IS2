from django.shortcuts import render, redirect, get_object_or_404

from .models import Usuario
from roles.models import CustomRole, UserCategoryRole
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
    return render(request, 'usuarios/manage_user.html', {'user': user, 'roles':user_roles})