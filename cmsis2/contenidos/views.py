from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContenidoForm, AprobarContenidoForm
from .models import Contenido, Plantilla
from django.utils import timezone


def seleccionar_plantilla(request, categoria_id):
    plantillas = Plantilla.objects.all()

    return render(request, 'contenidos/seleccionar_plantilla.html', {'plantillas': plantillas, 'categoria': categoria_id})


def previsualizar(request, plantilla_id):
    plantilla = Plantilla.objects.get(id=plantilla_id)
    return render(request, 'contenidos/previsualizar.html', {'plantilla': plantilla})


def crear_contenido(request, plantilla_id, categoria_id):
    page_title = 'Crear Contenido'

    #Traemos todas las subcategorias por categoria

    plantilla_predefinida = Plantilla.objects.get(id=plantilla_id)

    if request.method == 'POST':
        form = ContenidoForm(request.POST)

        if form.is_valid():
            nuevo_contenido = form.save(commit=False)
            nuevo_contenido.autor = request.user
            nuevo_contenido.estado = 'BORRADOR'
            nuevo_contenido.save()
            return redirect('ver_contenido', contenido_id=nuevo_contenido.id)

    else:
        form = ContenidoForm(initial={
            'cuerpo': plantilla_predefinida.plantilla,
        }, categoria_id=categoria_id)

    return render(request, 'contenidos/crear_contenido.html',
                  {
                      'page_title': page_title,
                      'form': form
                  })


def ver_contenido(request, contenido_id):
    contenido = get_object_or_404(Contenido, pk=contenido_id)

    return render(request, 'contenidos/ver_contenido.html',
                  {
                      'contenido': contenido
                  })


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
    contenidos = Contenido.objects.filter(estado='BORRADOR').order_by('-fecha_creacion')

    return render(request, 'contenidos/lista_contenidos.html',
                  {
                      'page_title': page_title,
                      'contenidos': contenidos
                  })


def ver_revision(request):
    page_title = 'En Revisión'
    contenidos = Contenido.objects.filter(estado='REVISION').order_by('-fecha_creacion')

    return render(request, 'contenidos/lista_contenidos.html',
                  {
                      'page_title': page_title,
                      'contenidos': contenidos
                  })


def ver_edicion(request):
    page_title = 'En Edición'
    contenidos = Contenido.objects.filter(estado='EDICION').order_by('-fecha_creacion')

    return render(request, 'contenidos/lista_contenidos.html',
                  {
                      'page_title': page_title,
                      'contenidos': contenidos
                  })


def ver_rechazados(request):
    page_title = 'Rechazados'
    contenidos = Contenido.objects.filter(estado='RECHAZADO').order_by('-fecha_creacion')

    return render(request, 'contenidos/lista_contenidos.html',
                  {
                      'page_title': page_title,
                      'contenidos': contenidos
                  })


def ver_inactivos(request):
    page_title = 'Inactivos'
    contenidos = Contenido.objects.filter(estado='INACTIVO').order_by('-fecha_creacion')

    return render(request, 'contenidos/lista_contenidos.html',
                  {
                      'page_title': page_title,
                      'contenidos': contenidos
                  })


def ver_publicados(request):
    page_title = 'Publicados'
    contenidos = Contenido.objects.filter(estado='PUBLICADO').order_by('-fecha_creacion')

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
            contenido.estado = 'PUBLICADO'
            contenido.fecha_publicacion = timezone.now()
            contenido.fecha_caducidad = form.cleaned_data['fecha_caducidad']
            contenido.save()
            return redirect('ver_contenido', contenido_id=contenido_id)
    else:
        form = AprobarContenidoForm()

    return render(request, 'contenidos/aprobar_contenido.html', {'form': form, 'contenido': contenido})


def rechazar_contenido(request, contenido_id):
    contenido = Contenido.objects.get(pk=contenido_id)
    contenido.estado = 'RECHAZADO'
    contenido.save()
    return redirect('ver_contenido', contenido_id=contenido_id)


def enviar_edicion(request, contenido_id):
    contenido = Contenido.objects.get(pk=contenido_id)
    contenido.estado = 'EDICION'
    contenido.save()
    return redirect('gest_contenidos')


def enviar_revision(request, contenido_id):
    contenido = Contenido.objects.get(pk=contenido_id)
    contenido.estado = 'REVISION'
    contenido.save()
    return redirect('gest_contenidos')
