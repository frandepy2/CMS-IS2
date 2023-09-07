from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoriaForm, SubcategoriaForm
from .models import Categoria, Subcategoria
from django.core.paginator import Paginator, Page
from decorators import has_permission_decorator
from django.contrib.auth.decorators import login_required

"""Crea la vista de la pantalla inicial de la sección categorías, donde se se listan todas las categorías existentes"""
@login_required
@has_permission_decorator('view_category')
def categorias(request):
    list_categorias = Categoria.objects.all().order_by('id')  # Obtén todos los roles
    paginator = Paginator(list_categorias,5)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'categorias/categorias.html', {'page': page})

"""Crea una categoría"""
@login_required
@has_permission_decorator('create_category')
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/crear_categoria.html', {'form': form})

"""Visualiza el estado de la categoría, cuales son las subcategorías asociadas a la categoría"""
@login_required
@has_permission_decorator('view_category')
def mas_informacion_categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    subcategorias = Subcategoria.objects.filter(categoria=categoria)
    return render(request, 'categorias/more_info.html', {'categoria': categoria, 'subcategorias': subcategorias})

"""Permite cambiar los detalles de la categpría seleccionada como descripción, inactivar o el nombre"""
@login_required
@has_permission_decorator('edit_category')
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categorias')  # Redirect to the list of roles
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'categorias/editar_categoria.html', {'form': form, 'categoria': categoria})

"""Permite inactivar la categoría"""
@login_required
@has_permission_decorator('inactivate_category')
def inactivar_categoria(request,categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if categoria.is_active :
        categoria.is_active = False
    else:
        categoria.is_active = True
    categoria.save()
    return redirect('categorias')

"""Crea la vista de subcategorías pertenecientes a una categoría. """
@login_required
@has_permission_decorator('edit_category')
def subcategorias(request):
    list_subcategorias = Subcategoria.objects.all().order_by('id')  # Obtén todos los roles
    paginator = Paginator(list_subcategorias,5)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'categorias/subcategorias.html', {'page': page})

"""Crea una subcategoría"""
@login_required
@has_permission_decorator('edit_category')
def crear_subcategoria(request):
    if request.method == 'POST':
        form = SubcategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subcategorias')  # Redirige a la vista deseada después de crear las subcategorias
    else:
        form = SubcategoriaForm()
    return render(request, 'categorias/crear_subcategoria.html', {'form': form})

"""Visualiza el estado de la subcategoría"""
@login_required
@has_permission_decorator('edit_category')
def mas_informacion_subcategoria(request, subcategoria_id):
    subcategoria = Subcategoria.objects.get(id=subcategoria_id)
    return render(request, 'categorias/more_info_subcategoria.html', {'subcategoria': subcategoria})

"""Permite editar el estado de una subcategoría"""
@login_required
@has_permission_decorator('edit_category')
def editar_subcategoria(request, subcategoria_id):
    subcategoria = get_object_or_404(Subcategoria, id=subcategoria_id)

    if request.method == 'POST':
        form = SubcategoriaForm(request.POST, instance=subcategoria)
        if form.is_valid():
            form.save()
            return redirect('subcategorias')  # Redirect to the list of subcategorias
    else:
        form = SubcategoriaForm(instance=subcategoria)

    return render(request, 'categorias/editar_subcategoria.html', {'form': form, 'subcategoria': subcategoria})

"""Permite inactivar una subcategoría"""
@login_required
@has_permission_decorator('edit_category')
def inactivar_subcategoria(request,subcategoria_id):
    subcategoria = get_object_or_404(Subcategoria, id=subcategoria_id)
    if subcategoria.is_active :
        subcategoria.is_active = False
    else:
        subcategoria.is_active = True
    subcategoria.save()
    return redirect('subcategorias')

