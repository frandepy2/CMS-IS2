from django.shortcuts import render,redirect
from .models import Plantilla
from .forms import ContenidoForm


def seleccionar_plantilla(request, categoria_id):
    plantillas = Plantilla.objects.all()

    return render(request, 'contenidos/seleccionar_plantilla.html', {'plantillas': plantillas, 'categoria': categoria_id})


def previsualizar(request, plantilla_id):
    plantilla = Plantilla.objects.get(id=plantilla_id)
    return render(request, 'contenidos/previsualizar.html', {'plantilla': plantilla})


def crear_contenido(request, plantilla_id, categoria_id):

    #Traemos todas las subcategorias por categoria

    plantilla_predefinida = Plantilla.objects.get(id=plantilla_id)

    if request.method == 'POST':
        form = ContenidoForm(request.POST)

        if form.is_valid():
            nuevo_contenido = form.save(commit=False)
            nuevo_contenido.estado = "CREATED"
            nuevo_contenido.autor = request.user
            nuevo_contenido.save()
            return redirect('/plantillas')

    else:
        form = ContenidoForm(initial={
            'cuerpo': plantilla_predefinida.plantilla,
        }, categoria_id=categoria_id)

    return render(request, 'contenidos/crear_contenido.html', {'form': form})


