from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoriaForm
from .models import Categoria
from django.core.paginator import Paginator, Page

# Create your views here.
def categorias(request):
    list_categorias = Categoria.objects.all().order_by('id')  # Obtén todos los roles
    paginator = Paginator(list_categorias,5)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'categorias/categorias.html', {'page': page})

def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias')  # Redirige a la vista deseada después de crear el rol
    else:
        form = CategoriaForm()
    return render(request, 'categorias/crear_categoria.html', {'form': form})

def mas_informacion_categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    return render(request, 'categorias/more_info.html', {'categoria': categoria})

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

def inactivar_categoria(request,categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if categoria.is_active :
        categoria.is_active = False
    else:
        categoria.is_active = True
    categoria.save()
    return redirect('categorias')
