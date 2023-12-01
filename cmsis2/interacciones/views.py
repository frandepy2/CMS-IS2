from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from contenidos.models import Contenido
from .forms import ComentarioForm
from .models import Accion
from django.shortcuts import redirect

from notificaciones.utils import crear_notificacion


@login_required
def crear_comentario(request, contenido_id):
    """
    Crea un comentario para un contenido específico.

    :param request: HttpRequest object
    :param contenido_id: ID del contenido al que se le quiere agregar el comentario
    :return: Redirección a la vista del contenido
    """
    contenido = Contenido.objects.get(id=contenido_id)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)

        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.contenido = contenido
            comentario.autor = request.user
            comentario.save()

            if contenido.cantidad_comentarios is None:
                contenido.cantidad_comentarios = 0
                contenido.save()

            contenido.cantidad_comentarios += 1
            contenido.save()

            crear_notificacion(
                emisor=request.user,
                receptor=contenido.autor,
                contenido=contenido,
                titulo=f"Nuevo comentario",
                mensaje=f"{comentario.autor.username} agrego un nuevo comentario en tu contenido {contenido.nombre}"
            )

            return redirect('ver_contenido', contenido_id = contenido_id)
        else:
            return redirect('ver_contenido', contenido_id = contenido_id)

@login_required
def dar_me_gusta(request, contenido_id):
    """
    Permite a un usuario autenticado dar "Me gusta" a un contenido.

    :param request: HttpRequest object
    :param contenido_id: ID del contenido al que se le quiere dar "Me gusta"
    :return: Redirección a la vista del contenido
    """
    contenido = Contenido.objects.get(id=contenido_id)
    usuario = request.user

    # Verifica si el usuario ya dio "Me gusta" a este contenido
    if not Accion.objects.filter(usuario=usuario, contenido=contenido, tipo_accion='LIKE').exists():
        accion = Accion(usuario=usuario, contenido=contenido, tipo_accion='LIKE') #LIKE INDICA UN MEGUSTA
        accion.save()

        if contenido.cantidad_me_gusta is None:
            contenido.cantidad_me_gusta = 0
            contenido.save()

        contenido.cantidad_me_gusta += 1
        contenido.save()

        crear_notificacion(
            emisor=request.user,
            receptor=contenido.autor,
            contenido=contenido,
            titulo=f"Nuevo Like",
            mensaje=f"{request.user.username} dio like a tu contenido {contenido.nombre}"
        )

    return redirect('ver_contenido', contenido_id = contenido_id)  # Redirige al usuario a la página del contenido


def compartir_contenido(request, contenido_id):
    """
    Permite a un usuario compartir un contenido. Si el usuario no está autenticado, aún puede compartir.

    :param request: HttpRequest object
    :param contenido_id: ID del contenido que se quiere compartir
    :return: JsonResponse con un mensaje y la URI del contenido
    """
    contenido = Contenido.objects.get(id=contenido_id)

    if not request.user.is_authenticated:
        accion = Accion(contenido=contenido, tipo_accion='SHARE')
        accion.save()
    else:
        accion = Accion(usuario=request.user, contenido=contenido, tipo_accion='SHARE')
        accion.save()

    if contenido.cantidad_compartir is None:
        contenido.cantidad_compartir = 0
        contenido.save()

    contenido.cantidad_compartir += 1
    contenido.save()
    uri_anterior = request.META.get('HTTP_REFERER', 'No disponible')
    alert_message = f"Link {uri_anterior} copiado en el portapapeles."

    return JsonResponse({'alert_message': alert_message, 'uri_copiar':uri_anterior })
