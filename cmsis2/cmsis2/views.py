from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.generic import TemplateView
from categorias.models import Categoria
from contenidos.models import Contenido
from notificaciones.models import Notificacion


def HomeView(request):
    page_title = "Ultimas Entradas"

    contenidos = Contenido.objects.filter(estado='PUBLICADO').order_by('-fecha_publicacion')

    return render(request, 'home/home.html',
                  {
                      'page_title': page_title,
                      'contenidos': contenidos,
                  })
