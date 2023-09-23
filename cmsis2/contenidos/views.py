from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContenidoForm
from .models import Contenido


# Create your views here.
def crear_contenido(request):
    if request.method == 'POST':
        form = ContenidoForm(request.POST)
        if form.is_valid():
            contenido = form.save(commit=False)  # No guardes el objeto en la base de datos todavía
            if request.user.is_authenticated:
                contenido.autor = request.user  # Asigna el usuario autenticado como autor del contenido
                contenido.estado = 'CREATED'
                contenido.save()  # Guarda el objeto en la base de datos
                return redirect('preview_contenido', contenido_id=contenido.id)
    else:
        form = ContenidoForm()

    return render(request, 'contenidos/crear_contenido.html', {'form': form})


def ver_contenido(request, contenido_id):
    contenido = get_object_or_404(Contenido, pk=contenido_id)
    return render(request, 'contenidos/ver_contenido.html',
                  {
                      'contenido': contenido
                  })


def preview_contenido(request, contenido_id):
    contenido = get_object_or_404(Contenido, pk=contenido_id)
    return render(request, 'contenidos/preview_contenido.html', {'contenido':contenido})


def editar_contenido(request, contenido_id):
    contenido = get_object_or_404(Contenido, pk=contenido_id)

    if request.method == 'POST':
        form = ContenidoForm(request.POST, instance=contenido)
        if form.is_valid():
            form.save()
            return redirect('preview_contenido', contenido_id=contenido.id)
    else:
        form = ContenidoForm(instance=contenido)

    return render(request, 'contenidos/editar_contenido.html', {'form': form, 'contenido': contenido})
