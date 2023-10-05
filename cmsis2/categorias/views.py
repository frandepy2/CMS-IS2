from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import CategoriaForm, SubcategoriaForm
from .models import Categoria, Subcategoria
from django.core.paginator import Paginator, Page
from decorators import has_permission_decorator, has_some_cat_role_decorator
from django.contrib.auth.decorators import login_required
from roles.models import UserCategoryRole
from roles.forms import UserCategoryRoleForm
from contenidos.models import Contenido

"""Crea la vista de la pantalla inicial de la sección categorías, donde se se listan todas las categorías existentes"""


@login_required
@has_permission_decorator('view_category')
def categorias(request):
    page_title = 'Categorias'
    list_categorias = Categoria.objects.all().order_by('id')  # Obtén todos los roles
    paginator = Paginator(list_categorias, 5)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'categorias/categorias.html',
                  {
                      'page_title': page_title,
                      'page': page
                  })


"""Crea una categoría"""


@login_required
@has_permission_decorator('create_category')
def crear_categoria(request):
    page_title = 'Crear Nueva Categoria'
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/crear_categoria.html',
                  {
                      'page_title': page_title,
                      'form': form
                  })


"""Visualiza el estado de la categoría, cuales son las subcategorías asociadas a la categoría"""


@login_required
@has_permission_decorator('view_category')
def mas_informacion_categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    page_title = categoria.nombre
    subcategorias = Subcategoria.objects.filter(categoria=categoria)

    #    usuarios = Usuario.objects.filter(usercategoryrole__category_id=categoria_id)
    usuarios_roles = UserCategoryRole.objects.filter(category_id=categoria_id)

    return render(request, 'categorias/more_info.html',
                  {
                      'page_title': page_title,
                      'categoria': categoria,
                      'subcategorias': subcategorias,
                      'users_roles': usuarios_roles
                  })


"""Permite cambiar los detalles de la categpría seleccionada como descripción, inactivar o el nombre"""


@login_required
@has_permission_decorator('edit_category')
def editar_categoria(request, categoria_id):
    page_title = 'Modificar Categoria'

    categoria = get_object_or_404(Categoria, id=categoria_id)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categorias')  # Redirect to the list of roles
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'categorias/editar_categoria.html',
                  {
                      'page_title': page_title,
                      'form': form,
                      'categoria': categoria
                  })


"""Permite inactivar la categoría"""


@login_required
@has_permission_decorator('inactivate_category')
def inactivar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if categoria.is_active:
        categoria.is_active = False
    else:
        categoria.is_active = True
    categoria.save()
    return redirect('categorias')


"""Crea la vista de subcategorías pertenecientes a una categoría. """


@login_required
@has_permission_decorator('view_category')
def subcategorias(request):
    page_title = 'Subcategorias'
    list_subcategorias = Subcategoria.objects.all().order_by('id')  # Obtén todos los roles
    paginator = Paginator(list_subcategorias, 5)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'categorias/subcategorias.html',
                  {
                      'page_title': page_title,
                      'page': page
                  })


"""Crea una subcategoría"""


@login_required
@has_permission_decorator('edit_category')
def crear_subcategoria(request):
    page_title = 'Crear Nueva Subcategoria'
    if request.method == 'POST':
        form = SubcategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subcategorias')  # Redirige a la vista deseada después de crear las subcategorias
    else:
        form = SubcategoriaForm()
    return render(request, 'categorias/crear_subcategoria.html',
                  {
                      'page_title': page_title,
                      'form': form
                  })


"""Visualiza el estado de la subcategoría"""


@login_required
@has_permission_decorator('edit_category')
def mas_informacion_subcategoria(request, subcategoria_id):
    subcategoria = Subcategoria.objects.get(id=subcategoria_id)
    page_title = subcategoria.nombre
    return render(request, 'categorias/more_info_subcategoria.html',
                  {
                      'page_title': page_title,
                      'subcategoria': subcategoria
                  })


"""Permite editar el estado de una subcategoría"""


@login_required
@has_permission_decorator('edit_category')
def editar_subcategoria(request, subcategoria_id):
    page_title = 'Modificar Subcategoria'
    subcategoria = get_object_or_404(Subcategoria, id=subcategoria_id)

    if request.method == 'POST':
        form = SubcategoriaForm(request.POST, instance=subcategoria)
        if form.is_valid():
            form.save()
            return redirect('subcategorias')  # Redirect to the list of subcategorias
    else:
        form = SubcategoriaForm(instance=subcategoria)

    return render(request, 'categorias/editar_subcategoria.html',
                  {
                      'page_title': page_title,
                      'form': form,
                      'subcategoria': subcategoria
                  })


"""Permite inactivar una subcategoría"""


@login_required
@has_permission_decorator('edit_category')
def inactivar_subcategoria(request, subcategoria_id):
    subcategoria = get_object_or_404(Subcategoria, id=subcategoria_id)
    if subcategoria.is_active:
        subcategoria.is_active = False
    else:
        subcategoria.is_active = True
    subcategoria.save()
    return redirect('subcategorias')


"""Permite agregar usuarios a una categoria"""


@login_required
@has_permission_decorator('add_user')
def agregar_usuario(request, categoria_id):
    category = Categoria.objects.get(id=categoria_id)
    page_title = 'Agregar usuario a categoria'

    if request.method == 'POST':
        form = UserCategoryRoleForm(request.POST, category=category)
        if form.is_valid():
            form.save()
            target_url = reverse('mas_informacion_categoria', kwargs={'categoria_id': categoria_id})
            return redirect(target_url)
    else:
        form = UserCategoryRoleForm()
        form.fields['category'].initial = category
        form.fields['category'].widget.attrs['disabled'] = True
    return render(request, 'usuarios/asign_user_role.html',
                  {
                      'page_title': page_title,
                      'form': form
                  })


"""Permite quitar a usuarios de una categoria"""


@login_required
@has_permission_decorator('delete_user')
def quitar_usuario(request, role_category_id):
    role_category = get_object_or_404(UserCategoryRole, id=role_category_id)

    categoria_id = role_category.category.id

    role_category.delete()

    target_url = reverse('mas_informacion_categoria', kwargs={'categoria_id': categoria_id})
    return redirect(target_url)


"""Muestra el contenido de una categoria especifica para cualquier usuario"""


def ver_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    page_title = categoria.nombre
    subcategorias = Subcategoria.objects.filter(categoria=categoria, is_active=True)
    contenidos = Contenido.objects.filter(subcategoria__categoria=categoria, estado='PUBLICADO').order_by(
        '-fecha_publicacion')
    categorias = Categoria.objects.filter(is_active=True)

    return render(request, 'categorias/ver_contenidos_categoria.html', {
        'page_title': page_title,
        'categoria': categoria,
        'subcategorias': subcategorias,
        'contenidos': contenidos,
        'categorias': categorias
    })


def ver_subcategoria(request, subcategoria_id):
    subcategoria_act = get_object_or_404(Subcategoria, pk=subcategoria_id)
    categoria = Categoria.objects.get(id=subcategoria_act.categoria.id)
    page_title = categoria.nombre + ': ' + subcategoria_act.nombre
    subcategorias = Subcategoria.objects.filter(categoria=categoria, is_active=True)
    contenidos = Contenido.objects.filter(subcategoria=subcategoria_act, estado='PUBLICADO').order_by(
        '-fecha_publicacion')
    categorias = Categoria.objects.filter(is_active=True)

    return render(request, 'categorias/ver_contenidos_subcategoria.html', {
        'page_title': page_title,
        'categoria': categoria,
        'subcategoria_act': subcategoria_act,
        'subcategorias': subcategorias,
        'contenidos': contenidos,
        'categorias': categorias
    })


@login_required
@has_some_cat_role_decorator()
def mostrar_kanban(request, categoria_id):
    category = get_object_or_404(Categoria, id=categoria_id)

    list_subcategorias = Subcategoria.objects.filter(categoria=category)

    list_contenidos = []

    # Recorrer todas las subcategorías
    for subcategoria in list_subcategorias:
        # Obtener todos los contenidos asociados a la subcategoría actual
        contenidos_subcategoria = Contenido.objects.filter(subcategoria=subcategoria)

        # Agregar los contenidos de esta subcategoría a la lista general de contenidos
        list_contenidos.extend(contenidos_subcategoria)

    # Supongamos que tienes list_contenidos con todos los contenidos de las subcategorías

    # Crear un diccionario para almacenar listas de contenidos por estado
    contenidos_por_estado = {
        'BORRADOR': [],
        'EDICION': [],
        'REVISION': [],
        'PUBLICADO': [],
        'RECHAZADO': [],
    }

    # Recorrer list_contenidos y asignar cada contenido a la lista correspondiente en el diccionario
    for contenido in list_contenidos:
        estado = contenido.estado  # Supongo que 'estado' es el campo que indica el estado del contenido
        if estado in contenidos_por_estado:
            contenidos_por_estado[estado].append(contenido)

    # Ahora, contenidos_por_estado contiene las listas de contenidos separadas por estado
    borradores = contenidos_por_estado['BORRADOR']
    ediciones = contenidos_por_estado['EDICION']
    revisiones = contenidos_por_estado['REVISION']
    publicados = contenidos_por_estado['PUBLICADO']
    rechazados = contenidos_por_estado['RECHAZADO']

    # Asegúrate de que list_subcategorias contenga las subcategorias que deseas mostrar en el kanban.

    return render(request, 'contenidos/kanban.html', {
        'category': category,
        'list_subcategorias': list_subcategorias,
        'borradores': borradores,
        'revisiones': revisiones,
        'ediciones': ediciones,
        'publicados': publicados,
        'rechazados': rechazados
    })
