from django.shortcuts import render
from django.http import JsonResponse
from categorias.models import Categoria, Subcategoria
from interacciones.models import Accion
from contenidos.models import Contenido
from django.db.models import Count

# Create your views here.
def mostrar_reportes(request):
    return render(request, 'reportes/reportes.html')

def interacciones_por_categoria(request):
    #Traemos todas las categorias
    categorias = Categoria.objects.all()
    interacciones_por_categoria = {}
    #traemos todas las subcategorias de cada categoria
    for categoria in categorias:
        contenidos_en_categoria = Contenido.objects.filter(subcategoria__categoria=categoria)

        total_interacciones = 0

        for contenido in contenidos_en_categoria:

            interacciones_contenido = Accion.objects.filter(contenido=contenido).count()

            total_interacciones +=interacciones_contenido

        interacciones_por_categoria[categoria.nombre] = total_interacciones

    return JsonResponse(interacciones_por_categoria)


def reportes_por_categoria(request):
    #Traemos todas las categorias
    categorias = Categoria.objects.all()
    interacciones_por_categoria = {}
    #traemos todas las subcategorias de cada categoria
    for categoria in categorias:
        contenidos_en_categoria = Contenido.objects.filter(subcategoria__categoria=categoria)

        total_interacciones = 0

        for contenido in contenidos_en_categoria:

            interacciones_contenido = Accion.objects.filter(contenido=contenido,tipo_accion='REPORT').count()

            total_interacciones +=interacciones_contenido

        interacciones_por_categoria[categoria.nombre] = total_interacciones

    return JsonResponse(interacciones_por_categoria)


def visualizaciones_por_categoria_por_fecha(request):
    tipo_accion = 'VIEW'  # Cambia el tipo de acción según tus necesidades
    data = get_interacciones_por_categoria(tipo_accion)
    return JsonResponse(data)

def likes_por_categoria_por_fecha(request):
    tipo_accion = 'LIKE'  # Cambia el tipo de acción según tus necesidades
    data = get_interacciones_por_categoria(tipo_accion)
    return JsonResponse(data)

def get_interacciones_por_categoria(tipo_accion):
    categorias = Categoria.objects.all()
    interacciones_por_categoria = {}

    for categoria in categorias:
        vistas_por_categoria = {}
        contenidos_en_categoria = Contenido.objects.filter(subcategoria__categoria=categoria)

        for contenido in contenidos_en_categoria:
            vistas = Accion.objects.filter(contenido=contenido, tipo_accion=tipo_accion)

            for vista in vistas:
                fecha = vista.fecha_creacion.date()
                fecha_str = fecha.strftime('%Y/%m/%d')

                if fecha_str not in vistas_por_categoria:
                    vistas_por_categoria[fecha_str] = 0

                vistas_por_categoria[fecha_str] += 1

        interacciones_por_categoria[categoria.nombre] = vistas_por_categoria

    return interacciones_por_categoria