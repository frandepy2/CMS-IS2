from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContenidoForm, AprobarContenidoForm
from .models import Contenido
from django.utils import timezone


# Create your views here.
def crear_contenido(request):
    if request.method == 'POST':
        form = ContenidoForm(request.POST)
        if form.is_valid():
            contenido = form.save(commit=False)  # No guardes el objeto en la base de datos todavía
            if request.user.is_authenticated:
                contenido.autor = request.user  # Asigna el usuario autenticado como autor del contenido
                contenido.estado = 'borrador'
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
            return redirect('ver_contenido', contenido_id=contenido.id)
    else:
        form = ContenidoForm(instance=contenido)

    return render(request, 'contenidos/editar_contenido.html', {'form': form, 'contenido': contenido})


def gest_contenidos(request):
    page_title = 'Gestión de Contenidos'
    return render(request, 'contenidos/gest_contenidos.html', {'page_title': page_title})


def ver_borrador(request):
    page_title = 'En Borrador'
    contenidos = Contenido.objects.filter(estado='borrador').order_by('-fecha_creacion')

    return render(request, 'contenidos/lista_contenidos.html',
                  {
                      'page_title': page_title,
                      'contenidos': contenidos
                  })


def ver_revision(request):
    page_title = 'En Revisión'
    contenidos = Contenido.objects.filter(estado='revision').order_by('-fecha_creacion')

    return render(request, 'contenidos/lista_contenidos.html',
                  {
                      'page_title': page_title,
                      'contenidos': contenidos
                  })


def ver_rechazados(request):
    page_title = 'Rechazados'
    contenidos = Contenido.objects.filter(estado='rechazado').order_by('-fecha_creacion')

    return render(request, 'contenidos/lista_contenidos.html',
                  {
                      'page_title': page_title,
                      'contenidos': contenidos
                  })


def ver_inactivos(request):
    page_title = 'Inactivos'
    contenidos = Contenido.objects.filter(estado='inactivo').order_by('-fecha_creacion')

    return render(request, 'contenidos/lista_contenidos.html',
                  {
                      'page_title': page_title,
                      'contenidos': contenidos
                  })


def ver_publicados(request):
    page_title = 'Publicados'
    contenidos = Contenido.objects.filter(estado='publicado').order_by('-fecha_creacion')

    return render(request, 'contenidos/lista_contenidos.html',
                  {
                      'page_title': page_title,
                      'contenidos': contenidos
                  })


def aprobar_contenido(request, contenido_id):

    contenido = Contenido.objects.get(pk=contenido_id)

    if request.method == 'POST':
        form = AprobarContenidoForm(request.POST)
        if form.is_valid():
            contenido.estado = 'publicado'
            contenido.fecha_publicacion = timezone.now()
            contenido.fecha_caducidad = form.cleaned_data['fecha_caducidad']
            contenido.save()
            return redirect('ver_contenido', contenido_id=contenido_id)
    else:
        form = AprobarContenidoForm()

    return render(request, 'contenidos/aprobar_contenido.html', {'form': form, 'contenido': contenido})


def rechazar_contenido(request, contenido_id):
    contenido = Contenido.objects.get(pk=contenido_id)
    contenido.estado = 'rechazado'
    contenido.save()
    return redirect('preview_contenido', contenido_id=contenido_id)