from django.shortcuts import render, redirect
from .models import Parametro

def lista_y_editar_parametros(request, parametro_id=None):
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