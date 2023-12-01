from notificaciones.models import Notificacion
from categorias.models import Categoria


def notificaciones(request):
    # Lógica para obtener las notificaciones
    notificaciones = []

    if request.user.is_authenticated:
        notificaciones = Notificacion.objects.filter(receptor=request.user).order_by('-fecha')

    return {'notificaciones': notificaciones}


def categorias(request):
    categorias = Categoria.objects.filter(is_active=True)

    return {'categorias': categorias}

