from django.shortcuts import render,redirect
from .models import Plantilla


def seleccionar_plantilla(request):
    # Recupera todas las plantillas desde la base de datos
    plantillas = Plantilla.objects.all()

    return render(request, 'contenidos/seleccionar_plantilla.html', {'plantillas': plantillas})


def previsualizar(request, plantilla_id):
    plantilla = Plantilla.objects.get(id=plantilla_id)
    return render(request, 'contenidos/previsualizar.html', {'plantilla': plantilla})
