from django.http import JsonResponse
from contenidos.models import Contenido
from .forms import ComentarioForm
from django.shortcuts import redirect

def crear_comentario(request, contenido_id):
    contenido = Contenido.objects.get(id=contenido_id)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)

        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.contenido = contenido
            comentario.autor = request.user
            comentario.save()

            return redirect('ver_contenido', contenido_id = contenido_id)
        else:
            return redirect('ver_contenido', contenido_id = contenido_id)