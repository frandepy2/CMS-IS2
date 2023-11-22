from .models import Notificacion


def crear_notificacion(emisor, receptor, accion=None, contenido=None, titulo=None, mensaje=None, leido=False):
    notificacion = Notificacion(
        emisor=emisor,
        receptor=receptor,
        accion=accion,
        contenido=contenido,
        titulo=titulo,
        mensaje=mensaje,
        leido=leido
    )
    notificacion.save()
    return notificacion