from django.http import JsonResponse
from contenidos.models import Contenido
from .forms import ComentarioForm
from .models import Accion
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

            if contenido.cantidad_comentarios is None:
                contenido.cantidad_comentarios = 0
                contenido.save()

            contenido.cantidad_comentarios += 1
            contenido.save()

            return redirect('ver_contenido', contenido_id = contenido_id)
        else:
            return redirect('ver_contenido', contenido_id = contenido_id)


def dar_me_gusta(request, contenido_id):
    contenido = Contenido.objects.get(id=contenido_id)
    usuario = request.user

    # Verifica si el usuario ya dio "Me gusta" a este contenido
    if not Accion.objects.filter(usuario=usuario, contenido=contenido, tipo_accion='LIKE').exists():
        accion = Accion(usuario=usuario, contenido=contenido, tipo_accion='LIKE') #LIKE INDICA UN MEGUSTA
        accion.save()

        if contenido.cantidad_me_gusta is None:
            contenido.cantidad_me_gusta = 0
            contenido.save()

        contenido.cantidad_me_gusta += 1
        contenido.save()

    return redirect('ver_contenido', contenido_id = contenido_id)  # Redirige al usuario a la página del contenido