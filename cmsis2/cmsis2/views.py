from django.shortcuts import render
from django.views.generic import TemplateView
from categorias.models import Categoria
from contenidos.models import Contenido


def HomeView(request):
    page_title = "Ultimas Entradas"
    categorias = Categoria.objects.filter(is_active=True)
    contenidos = Contenido.objects.filter(estado='publicado').order_by('-fecha_creacion')
    return render(request, 'home/home.html',
                  {
                      'page_title': page_title,
                      'categorias': categorias,
                      'contenidos': contenidos
                  })
