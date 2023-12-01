from .models import Notificacion


def crear_notificacion(emisor, receptor, accion=None, contenido=None, titulo=None, mensaje=None, leido=False):
    """
    Crea y guarda una nueva notificación.

    :param emisor: El usuario que emite la notificación.
    :param receptor: El usuario que recibe la notificación.
    :param accion: La acción relacionada con la notificación (opcional).
    :param contenido: El contenido asociado con la notificación (opcional).
    :param titulo: El título de la notificación (opcional).
    :param mensaje: El mensaje de la notificación (opcional).
    :param leido: Indica si la notificación se marca como leída, por defecto es False.
    :return: La instancia de la notificación recién creada.
    """
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