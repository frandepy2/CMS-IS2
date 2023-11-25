from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Notificacion
from usuarios.models import Usuario

# Create your views here.
def obtener_notificaciones(request, usuario_id):
    """
    Obtiene todas las notificaciones para un usuario específico.

    :param request: La solicitud HTTP.
    :param usuario_id: El ID del usuario para el cual se obtienen las notificaciones.
    :return: Una respuesta JSON que contiene las notificaciones o un mensaje de error si el usuario no se encuentra.
    """
    try:
        #Obtenemos todas las notificaciones creadas para el usuario con usuario_id
        receptor = Usuario.objects.get(id=usuario_id)
        notificaciones = Notificacion.objects.filter(receptor = receptor)

        # Convertimos las notificaciones a un formato que pueda ser serializado en JSON
        lista_notificaciones = []
        for notificacion in notificaciones:
            lista_notificaciones.append({
                "id": notificacion.id,
                "emisor": notificacion.emisor.id if notificacion.emisor else None,
                "receptor": notificacion.receptor.id,
                "accion": notificacion.accion.id if notificacion.accion else None,
                "contenido": notificacion.contenido.id if notificacion.contenido else None,
                "titulo": notificacion.titulo,
                "mensaje": notificacion.mensaje,
                "fecha": notificacion.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "leido": notificacion.leido
            })

        return JsonResponse(lista_notificaciones, safe=False)

    except ObjectDoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)


def marcar_como_leido(request, notificacion_id):
    """
    Marca una notificación como leída.

    :param request: La solicitud HTTP.
    :param notificacion_id: El ID de la notificación que se marcará como leída.
    :return: Una respuesta HTTP indicando que la operación fue exitosa.
    """
    notificacion = Notificacion.objects.get(id=notificacion_id)
    notificacion.leido = True
    notificacion.save()
    return HttpResponse("OK", status=200)
