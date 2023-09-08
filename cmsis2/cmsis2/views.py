from django.shortcuts import render
from django.views.generic import TemplateView
from categorias.models import Categoria


def HomeView(request):
    page_title = "Ultimas Entradas"
    categorias = Categoria.objects.filter(is_active=True)
    #categorias = Categoria.objects.all()
    return render(request, 'home/home.html', {'page_title': page_title, 'categorias': categorias})
