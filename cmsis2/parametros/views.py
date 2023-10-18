from django.shortcuts import render, redirect
from .models import Parametro
from decorators import has_permission_decorator, has_some_cat_role_decorator
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import os

@login_required
@has_permission_decorator('manage_parameters')
def lista_y_editar_parametros(request, parametro_id=None):
    """
    Lista y Edita Parámetros

    Esta vista permite listar y editar parámetros en el sistema.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :param parametro_id: (Opcional) El ID del parámetro a editar.
    :type parametro_id: int
    :returns: Una respuesta HTTP con la lista de parámetros o el formulario de edición.
    :rtype: HttpResponse
    """
    parametros = Parametro.objects.all()
    parametro = None

    if parametro_id:
        parametro = Parametro.objects.get(id=parametro_id)

    if request.method == 'POST':
        if parametro:
            parametro.clave = request.POST['clave']
            parametro.valor = request.POST['valor']
            parametro.save()
        else:
            clave = request.POST['clave']
            valor = request.POST['valor']
            Parametro.objects.create(clave=clave, valor=valor)

        return redirect('lista_y_editar_parametros')

    return render(request, 'parametros/parametros.html', {'parametros': parametros, 'parametro': parametro})

@login_required
@has_permission_decorator('manage_parameters')
def upload_image(request):
    if request.method == 'POST' and request.FILES['imagen']:
        imagen = request.FILES['imagen']
        fs = FileSystemStorage()

        # Check if the file 'logo.jpg' exists and delete it
        if fs.exists('logo.jpg'):
            os.remove(fs.url('logo.jpg').lstrip('/'))  # Remove the file

        # Renombrar el archivo a 'logo.jpg'
        nombre_archivo = 'logo.jpg'
        fs.save(nombre_archivo, imagen)

    return redirect('lista_y_editar_parametros')

def verificar_logo(request):
    fs = FileSystemStorage()
    ruta = 'logo.jpg'
    archivo_existe = fs.exists(ruta)
    titulo = Parametro.objects.get(clave='TITULO')
    return JsonResponse({'existe': archivo_existe, 'titulo': titulo.valor})
