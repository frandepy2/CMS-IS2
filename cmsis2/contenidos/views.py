from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContenidoForm, AprobarContenidoForm
from .models import Contenido, Plantilla
from categorias.models import Categoria
from django.utils import timezone
from parametros.models import Parametro


def seleccionar_plantilla(request, categoria_id):
    """
    Vista para seleccionar una plantilla de contenido.

    Esta función recupera todas las plantillas disponibles y las muestra en una vista,
    junto con la categoría seleccionada.

    Args:
        request (HttpRequest): El objeto HttpRequest de la solicitud HTTP.
        categoria_id (int): El ID de la categoría para la cual se seleccionará una plantilla.

    Returns:
        HttpResponse: La página que muestra las plantillas disponibles y la categoría seleccionada.
    """
    plantillas = Plantilla.objects.all()

    return render(request, 'contenidos/seleccionar_plantilla.html', {'plantillas': plantillas, 'categoria': categoria_id})


def previsualizar(request, plantilla_id):
    """
    Vista para previsualizar una plantilla de contenido.

    Esta función recupera una plantilla específica según el ID proporcionado
    y la muestra en una vista de previsualización.

    Args:
        request (HttpRequest): El objeto HttpRequest de la solicitud HTTP.
        plantilla_id (int): El ID de la plantilla que se va a previsualizar.

    Returns:
        HttpResponse: La página que muestra la plantilla en modo de previsualización.
    """
    plantilla = Plantilla.objects.get(id=plantilla_id)
    return render(request, 'contenidos/previsualizar.html', {'plantilla': plantilla})


def crear_contenido(request, plantilla_id, categoria_id):
    """
    Vista para crear un nuevo contenido basado en una plantilla.

    Esta función permite al usuario crear un nuevo contenido utilizando una plantilla predefinida.
    Si se envía un formulario válido, se crea el contenido como borrador.

    Args:
        request (HttpRequest): El objeto HttpRequest de la solicitud HTTP.
        plantilla_id (int): El ID de la plantilla que se utilizará para crear el contenido.
        categoria_id (int): El ID de la categoría del contenido.

    Returns:
        HttpResponse: La página de creación de contenido con el formulario correspondiente.
    """
    page_title = 'Crear Contenido'

    #Traemos todas las subcategorias por categoria

    plantilla_predefinida = Plantilla.objects.get(id=plantilla_id)
    categoria = get_object_or_404(Categoria, pk=categoria_id)

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
                      'form': form,
                      'categoria': categoria
                  })


def ver_contenido(request, contenido_id):
    """
    Renderiza una vista que muestra el contenido especificado.

    Esta función recupera un objeto de contenido específico según el ID proporcionado
    y lo muestra en una plantilla de visualización.

    Args:
        request (HttpRequest): El objeto HttpRequest de la solicitud HTTP.
        contenido_id (int): El ID del contenido que se mostrará.

    Returns:
        HttpResponse: La plantilla renderizada que muestra el contenido.
    """
    contenido = get_object_or_404(Contenido, pk=contenido_id)

    return render(request, 'contenidos/ver_contenido.html',
                  {
                      'contenido': contenido
                  })


def editar_contenido(request, contenido_id):
    """
    Renderiza una vista para editar el contenido especificado.

    Esta función recupera un objeto de contenido específico según el ID proporcionado y
    permite al usuario editar sus detalles a través de un formulario.

    Args:
        request (HttpRequest): El objeto HttpRequest de la solicitud HTTP.
        contenido_id (int): El ID del contenido que se va a editar.

    Returns:
        HttpResponse: La página de edición del contenido o una redirección a la vista de visualización del contenido.
    """
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
    """
    Renderiza una vista para la gestión de contenidos.

    Esta función muestra una página para la gestión de contenidos con un título personalizado.

    Args:
        request (HttpRequest): El objeto HttpRequest de la solicitud HTTP.

    Returns:
        HttpResponse: La página de gestión de contenidos con el título especificado.
    """
    page_title = 'Gestión de Contenidos'
    return render(request, 'contenidos/gest_contenidos.html', {'page_title': page_title})


def ver_borrador(request):
    """
    Renderiza una vista que muestra contenidos en estado de borrador.

    Esta función recupera y muestra una lista paginada de contenidos en estado de borrador,
    ordenados por fecha de creación, y asigna un título a la página.

    Args:
        request (HttpRequest): El objeto HttpRequest de la solicitud HTTP.

    Returns:
        HttpResponse: La página que muestra la lista de contenidos en estado de borrador.
    """
    page_title = 'En Borrador'
    contenidos = Contenido.objects.filter(estado='BORRADOR').order_by('-fecha_creacion')
    contenidos_borrador = Contenido.objects.filter(estado='BORRADOR').order_by('-fecha_creacion')

    return render(request, 'contenidos/lista_contenidos.html',
                  {
                      'page_title': page_title,
                      'contenidos_borrador': contenidos_borrador,
                      'contenidos': contenidos,
                  })


def ver_revision(request):
    """
    Renderiza una vista que muestra contenidos en estado de revisión.

    Esta función recupera y muestra una lista paginada de contenidos en estado de revisión,
    ordenados por fecha de creación, y asigna un título a la página.

    Args:
        request (HttpRequest): El objeto HttpRequest de la solicitud HTTP.

    Returns:
        HttpResponse: La página que muestra la lista de contenidos en estado de revisión.
    """
    page_title = 'En Revisión'
    contenidos = Contenido.objects.filter(estado='REVISION').order_by('-fecha_creacion')

    return render(request, 'contenidos/lista_contenidos.html',
                  {
                      'page_title': page_title,
                      'contenidos': contenidos
                  })


def ver_edicion(request):
    """
    Renderiza una vista que muestra contenidos en estado de edición.

    Esta función recupera y muestra una lista paginada de contenidos en estado de edición,
    ordenados por fecha de creación, y asigna un título a la página.

    Args:
        request (HttpRequest): El objeto HttpRequest de la solicitud HTTP.

    Returns:
        HttpResponse: La página que muestra la lista de contenidos en estado de edición.
    """
    page_title = 'En Edición'
    contenidos = Contenido.objects.filter(estado='EDICION').order_by('-fecha_creacion')

    return render(request, 'contenidos/lista_contenidos.html',
                  {
                      'page_title': page_title,
                      'contenidos': contenidos
                  })


def ver_rechazados(request):
    """
    Renderiza una vista que muestra contenidos en estado de rechazados.

    Esta función recupera y muestra una lista paginada de contenidos en estado de rechazados,
    ordenados por fecha de creación, y asigna un título a la página.

    Args:
        request (HttpRequest): El objeto HttpRequest de la solicitud HTTP.

    Returns:
        HttpResponse: La página que muestra la lista de contenidos en estado de rechazados.
    """
    page_title = 'Rechazados'
    contenidos = Contenido.objects.filter(estado='RECHAZADO').order_by('-fecha_creacion')

    return render(request, 'contenidos/lista_contenidos.html',
                  {
                      'page_title': page_title,
                      'contenidos': contenidos
                  })


def ver_inactivos(request):
    """
    Renderiza una vista que muestra contenidos en estado de inactivos.

    Esta función recupera y muestra una lista paginada de contenidos en estado de inactivos,
    ordenados por fecha de creación, y asigna un título a la página.

    Args:
        request (HttpRequest): El objeto HttpRequest de la solicitud HTTP.

    Returns:
        HttpResponse: La página que muestra la lista de contenidos en estado de inactivos.
    """
    page_title = 'Inactivos'
    contenidos = Contenido.objects.filter(estado='INACTIVO').order_by('-fecha_creacion')

    return render(request, 'contenidos/lista_contenidos.html',
                  {
                      'page_title': page_title,
                      'contenidos': contenidos
                  })


def ver_publicados(request):
    """
    Renderiza una vista que muestra contenidos en estado de publicados.

    Esta función recupera y muestra una lista paginada de contenidos en estado de publicados,
    ordenados por fecha de creación, y asigna un título a la página.

    Args:
        request (HttpRequest): El objeto HttpRequest de la solicitud HTTP.

    Returns:
        HttpResponse: La página que muestra la lista de contenidos en estado de publicados.
    """
    page_title = 'Publicados'
    contenidos = Contenido.objects.filter(estado='PUBLICADO').order_by('-fecha_creacion')

    return render(request, 'contenidos/lista_contenidos.html',
                  {
                      'page_title': page_title,
                      'contenidos': contenidos
                  })


def aprobar_contenido(request, contenido_id):
    """
    Vista para aprobar el contenido especificado.

    Esta función permite aprobar el contenido especificado, cambiar su estado a 'PUBLICADO',
    establecer la fecha de publicación y la fecha de caducidad según los datos del formulario.

    Args:
        request (HttpRequest): El objeto HttpRequest de la solicitud HTTP.
        contenido_id (int): El ID del contenido que se va a aprobar.

    Returns:
        HttpResponse: Redirección a la vista de visualización del contenido aprobado.
    """
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
    """
    Vista para rechazar el contenido especificado.

    Esta función permite cambiar el estado del contenido especificado a 'RECHAZADO'.

    Args:
        request (HttpRequest): El objeto HttpRequest de la solicitud HTTP.
        contenido_id (int): El ID del contenido que se va a rechazar.

    Returns:
        HttpResponse: Redirección a la vista de visualización del contenido rechazado.
    """
    contenido = Contenido.objects.get(pk=contenido_id)
    contenido.estado = 'RECHAZADO'
    contenido.save()
    return redirect('ver_contenido', contenido_id=contenido_id)


def enviar_edicion(request, contenido_id):
    """
    Vista para enviar el contenido a estado de edición.

    Esta función permite cambiar el estado del contenido especificado a 'EDICION'.

    Args:
        request (HttpRequest): El objeto HttpRequest de la solicitud HTTP.
        contenido_id (int): El ID del contenido que se va a enviar a estado de edición.

    Returns:
        HttpResponse: Redirección a la vista de gestión de contenidos.
    """
    contenido = Contenido.objects.get(pk=contenido_id)
    contenido.estado = 'EDICION'
    contenido.save()
    return redirect('gest_contenidos')


def enviar_revision(request, contenido_id):
    """
    Vista para enviar el contenido a estado de revisión.

    Esta función permite cambiar el estado del contenido especificado a 'REVISION'.

    Args:
        request (HttpRequest): El objeto HttpRequest de la solicitud HTTP.
        contenido_id (int): El ID del contenido que se va a enviar a estado de revisión.

    Returns:
        HttpResponse: Redirección a la vista de gestión de contenidos.
    """
    contenido = Contenido.objects.get(pk=contenido_id)
    contenido.estado = 'REVISION'
    contenido.save()
    return redirect('gest_contenidos')

  
def denunciar_contenido(request, contenido_id):
    """
    Vista para reportar contenido como inapropiado.

    :param request: El objeto de solicitud HTTP.
    :param contenido_id: El ID del contenido a reportar.
    :return: Una redirección a la página de inicio.
    """
    contenido = Contenido.objects.get(pk=contenido_id)
    cant_max_denuncias = Parametro.objects.get(clave='MAX_CANT_DENUNCIAS')
    cant_denuncias_max = int(cant_max_denuncias.valor)

    if contenido.cantidad_denuncias is None:
        contenido.cantidad_denuncias = 0
        contenido.save()

    contenido.cantidad_denuncias += 1

    if (contenido.cantidad_denuncias >= cant_denuncias_max):
        contenido.estado = 'INACTIVO'

    contenido.save()

    return redirect('home')


def inactivar_contenido(request, contenido_id):
    """
    Vista para inactivar el contenido

    Esta función permite cambiar el estado del contenido especificado a 'INACTIVO'.

    Args:
        request (HttpRequest): El objeto HttpRequest de la solicitud HTTP.
        contenido_id (int): El ID del contenido que se va a enviar a estado de revisión.

    Returns:
        HttpResponse: Redirección a la vista de gestión de contenidos.
    """
    contenido = get_object_or_404(Contenido, pk=contenido_id)
    contenido.estado = 'INACTIVO'
    contenido.save()
    return redirect('gest_contenidos')
