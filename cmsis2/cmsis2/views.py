from django.shortcuts import render
from django.views.generic import TemplateView


def HomeView(request):
    page_title = "Ultimas Entradas"
    return render(request, 'home/home.html', {'page_title': page_title})