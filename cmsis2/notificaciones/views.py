from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Notificacion
from usuarios.models import Usuario

# Create your views here.
def obtener_notificaciones(request, usuario_id):
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
    notificacion = Notificacion.objects.get(id=notificacion_id)
    notificacion.leido = True
    notificacion.save()
    return HttpResponse("OK", status=200)
