from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from decorators import has_permission_decorator
from categorias.models import Categoria, Subcategoria #TODO quitar cmsis2
from interacciones.models import Accion #TODO quitar cmsis2
from contenidos.models import Contenido #TODO quitar cmsis2
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image,Paragraph,Spacer,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import matplotlib.pyplot as plt


# Create your views here.
@login_required
@has_permission_decorator('view_reports')
def mostrar_reportes(request):
    """
    Vista para mostrar la lista de reportes.

    Esta vista renderiza la página de reportes y se utiliza para mostrar una lista de reportes disponibles.
    Requiere que el usuario esté autenticado.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: La página de reportes.
    :rtype: HttpResponse
    """
    return render(request, 'reportes/reportes.html')

def calcular_interacciones_por_categoria():
    """
    Calcula el número total de interacciones por categoría.

    Esta función calcula el número total de interacciones por cada categoría, donde una interacción
    se refiere a la cantidad de acciones realizadas en contenido asociado a esa categoría.

    :return: Un diccionario que mapea el nombre de cada categoría al número total de interacciones.
    :rtype: dict
    """
    categorias = Categoria.objects.all()
    interacciones_por_categoria = {}

    for categoria in categorias:
        contenidos_en_categoria = Contenido.objects.filter(subcategoria__categoria=categoria)

        total_interacciones = 0

        for contenido in contenidos_en_categoria:
            interacciones_contenido = Accion.objects.filter(contenido=contenido).count()
            total_interacciones += interacciones_contenido

        interacciones_por_categoria[categoria.nombre] = total_interacciones

    return interacciones_por_categoria

def interacciones_por_categoria(request):
    """
    Vista para obtener el número total de interacciones por categoría y devolverlo como respuesta JSON.

    Esta vista utiliza la función 'calcular_interacciones_por_categoria' para calcular el número total de
    interacciones por categoría y luego devuelve este resultado como una respuesta JSON.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: Una respuesta JSON que contiene el número total de interacciones por categoría.
    :rtype: JsonResponse
    """
    interacciones = calcular_interacciones_por_categoria()
    return JsonResponse(interacciones)


def reportes_por_categoria(request):
    """
    Vista para obtener el número total de reportes por categoría y devolverlo como respuesta JSON.

    Esta vista obtiene el número total de reportes por categoría utilizando la función 'calcular_interacciones_por_categoria'
    y devuelve este resultado como una respuesta JSON. Los reportes se obtienen de los contenidos marcados con la acción 'REPORT'.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: Una respuesta JSON que contiene el número total de reportes por categoría.
    :rtype: JsonResponse
    """
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
    """
    Vista para obtener el número total de visualizaciones por categoría y fecha y devolverlo como respuesta JSON.

    Esta vista utiliza la función 'get_interacciones_por_categoria' para obtener el número total de visualizaciones por
    categoría y fecha. Puedes cambiar el valor de 'tipo_accion' según tus necesidades para obtener distintos tipos de acciones.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: Una respuesta JSON que contiene el número total de visualizaciones por categoría y fecha.
    :rtype: JsonResponse
    """
    tipo_accion = 'VIEW'  # Cambia el tipo de acción según tus necesidades
    data = get_interacciones_por_categoria(tipo_accion)
    return JsonResponse(data)

def likes_por_categoria_por_fecha(request):
    """
    Vista para obtener el número total de 'likes' por categoría y fecha y devolverlo como respuesta JSON.

    Esta vista utiliza la función 'get_interacciones_por_categoria' para obtener el número total de 'likes' por
    categoría y fecha. Puedes cambiar el valor de 'tipo_accion' según tus necesidades para obtener distintos tipos de acciones.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: Una respuesta JSON que contiene el número total de 'likes' por categoría y fecha.
    :rtype: JsonResponse
    """
    tipo_accion = 'LIKE'  # Cambia el tipo de acción según tus necesidades
    data = get_interacciones_por_categoria(tipo_accion)
    return JsonResponse(data)


def get_interacciones_por_categoria(tipo_accion):
    """
    Calcula el número total de interacciones de un tipo específico por categoría y fecha.

    Esta función calcula el número total de interacciones de un tipo específico (por ejemplo, 'vistas' o 'likes')
    por categoría y fecha. Los resultados se agrupan por categoría y se detallan por fecha.

    :param tipo_accion: El tipo de acción para el que se desean calcular las interacciones (por ejemplo, 'VIEW' o 'LIKE').
    :type tipo_accion: str
    :return: Un diccionario que mapea el nombre de cada categoría a un diccionario que contiene las interacciones por fecha.
    :rtype: dict
    """
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


@login_required
@has_permission_decorator('view_reports')
def generar_pdf(request):
    """
    Vista para generar un informe en formato PDF que contiene gráficos y tablas de interacciones por categoría y fecha.

    Esta vista crea un informe en formato PDF que incluye gráficos y tablas de interacciones por categoría y fecha,
    incluyendo visualizaciones y likes. Los gráficos y tablas se generan a partir de datos obtenidos mediante funciones
    como 'calcular_interacciones_por_categoria' y 'get_interacciones_por_categoria'.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :return: Un archivo PDF que contiene el informe de interacciones por categoría y fecha.
    :rtype: FileResponse (PDF)
    """
    # Crear un objeto BytesIO para capturar el PDF generado
    buffer = BytesIO()

    # Establecer el documento PDF con tamaño de página letter y orientación vertical
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    flowables = []

    # Establecer estilos
    styles = getSampleStyleSheet()

    # Titulo del reporte
    title = Paragraph("Reporte de Interacciones", styles['Heading1'])
    flowables.append(title)
    flowables.append(Spacer(1, 12))

    # 1. Gráfico: Interacciones por categoría
    interacciones = calcular_interacciones_por_categoria()
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(interacciones.keys(), interacciones.values(), color='blue')
    ax.set_title('Interacciones por categoría')
    ax.set_xlabel('Categoría')
    ax.set_ylabel('Cantidad de interacciones')
    plt.xticks(rotation=45, ha='right')
    imgdata = BytesIO()
    plt.tight_layout()
    plt.savefig(imgdata, format='png')  # Cambiamos a formato PNG
    imgdata.seek(0)
    img = Image(imgdata)
    flowables.append(img)

    data_interacciones = [['Categoría', 'Interacciones']]
    for cat, valor in interacciones.items():
        data_interacciones.append([cat, valor])
    t_interacciones = Table(data_interacciones, colWidths=[200, 100])
    t_interacciones.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                                          ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                          ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                          ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                          ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                          ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                          ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    flowables.append(t_interacciones)

    flowables.append(PageBreak())

    # Puedes seguir agregando más gráficos y contenido al PDF de manera similar...
    interacciones = get_interacciones_por_categoria('LIKE')
    categorias = list(interacciones.keys())
    totales_likes = [sum(valores.values()) for valores in interacciones.values()]

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(categorias, totales_likes, color='red')
    ax.set_title('Likes por categoría')
    ax.set_xlabel('Likes')
    ax.set_ylabel('Cantidad de Likes')
    plt.xticks(rotation=45, ha='right')
    imgdata = BytesIO()
    plt.tight_layout()
    plt.savefig(imgdata, format='png')  # Cambiamos a formato PNG
    imgdata.seek(0)
    img = Image(imgdata)
    flowables.append(img)

    # Tabla: Detalle de Likes por categoría
    data_likes = [['Categoría', 'Total Likes']]
    for cat, likes in zip(categorias, totales_likes):
        data_likes.append([cat, likes])
    t_likes = Table(data_likes, colWidths=[200, 100])
    t_likes.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.red),
                                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                 ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                 ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    flowables.append(t_likes)

    flowables.append(PageBreak())

    # 1. Gráfico: Visualizaciones por categoría por fecha
    visualizaciones_data = get_interacciones_por_categoria('VIEW')
    categorias = list(visualizaciones_data.keys())

    for categoria, fecha_data in visualizaciones_data.items():
        fechas = list(fecha_data.keys())
        visualizaciones = list(fecha_data.values())

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.bar(fechas, visualizaciones, color='green')
        ax.set_title(f'Visualizaciones por fecha en {categoria}')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Cantidad de visualizaciones')
        plt.xticks(rotation=45, ha='right')

        imgdata = BytesIO()
        plt.tight_layout()
        plt.savefig(imgdata, format='png')
        imgdata.seek(0)
        img = Image(imgdata)

        flowables.append(img)

        # Tabla: Detalle de Visualizaciones por fecha en categoría
        table_data = [['Fecha', 'Visualizaciones']]
        for date, view_count in fecha_data.items():
            table_data.append([date, view_count])

        t = Table(table_data, colWidths=[200, 100])
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.green),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        flowables.append(t)
        flowables.append(PageBreak())

    # 1. Gráfico: Likes por categoría por fecha
    likes_data = get_interacciones_por_categoria('LIKE')
    categorias = list(likes_data.keys())

    for categoria, fecha_data in likes_data.items():
        fechas = list(fecha_data.keys())
        likes = list(fecha_data.values())

        fig, ax = plt.subplots(figsize=(6, 3))
        ax.bar(fechas, likes, color='purple')
        ax.set_title(f'Likes por fecha en {categoria}')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Cantidad de Likes')
        plt.xticks(rotation=45, ha='right')

        imgdata = BytesIO()
        plt.tight_layout()
        plt.savefig(imgdata, format='png')
        imgdata.seek(0)
        img = Image(imgdata)

        flowables.append(img)

        # Tabla: Detalle de Likes por fecha en categoría
        table_data = [['Fecha', 'Likes']]
        for date, like_count in fecha_data.items():
            table_data.append([date, like_count])

        t = Table(table_data, colWidths=[200, 100])
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.purple),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        flowables.append(t)
        flowables.append(PageBreak())

    # Generar PDF
    doc.build(flowables)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='reporte_interacciones.pdf')

def contenido_to_json(contenido):
    """
    Convierte un objeto de contenido en un diccionario JSON.

    Esta función toma un objeto de contenido y lo convierte en un diccionario JSON que representa la información
    relevante del contenido. El diccionario incluye información como el nombre, autor, subcategoría, fechas,
    estado y estadísticas de interacción.

    :param contenido: El objeto de contenido a convertir en formato JSON.
    :type contenido: Contenido
    :return: Un diccionario JSON que representa la información del contenido.
    :rtype: dict
    """
    contenido_json = {
        'nombre': contenido.nombre,
        'autor': contenido.autor.username,  # Supongamos que el autor tiene un campo "nombre"
        'subcategoria': contenido.subcategoria.nombre,  # Supongamos que la subcategoría tiene un campo "nombre"
        'fecha_creacion': contenido.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),  # Formatea la fecha como una cadena
        'fecha_caducidad': contenido.fecha_caducidad.strftime('%Y-%m-%d') if contenido.fecha_caducidad else None,
        'fecha_publicacion': contenido.fecha_publicacion.strftime('%Y-%m-%d %H:%M:%S') if contenido.fecha_publicacion else None,
        'estado': contenido.estado,
        'cantidad_denuncias': contenido.cantidad_denuncias,
        'cantidad_me_gusta': contenido.cantidad_me_gusta,
        'cantidad_compartir': contenido.cantidad_compartir,
        'cantidad_comentarios': contenido.cantidad_comentarios,
        'cantidad_visualizaciones': contenido.cantidad_visualizaciones,
        'acciones': get_acciones_contenido(contenido),
    }
    return contenido_json


def get_acciones_contenido(contenido):
    """
    Obtiene las acciones asociadas a un contenido y las convierte en una lista de diccionarios JSON.

    Esta función toma un objeto de contenido y obtiene todas las acciones asociadas a ese contenido. Luego, las acciones
    se convierten en una lista de diccionarios JSON que incluyen información como el usuario que realizó la acción, el tipo
    de acción y la fecha de creación.

    :param contenido: El objeto de contenido del que se desean obtener las acciones.
    :type contenido: Contenido
    :return: Una lista de diccionarios JSON que representan las acciones asociadas al contenido.
    :rtype: list
    """
    acciones = contenido.acciones.all()
    acciones_json = []
    for accion in acciones:
        accion_dict = {
            'usuario':  accion.usuario.username if accion.usuario else None,
            'tipo_accion': accion.tipo_accion,
            'fecha_creacion': accion.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
        }
        acciones_json.append(accion_dict)

    return acciones_json


def interacciones_categoria_json(category_id):
    """
    Obtiene información detallada de los contenidos de una categoría en formato JSON.

    Esta función toma un ID de categoría y devuelve un diccionario JSON que contiene información detallada de todos los contenidos
    pertenecientes a esa categoría. La información incluye detalles como el nombre, autor, subcategoría, fechas, estado y estadísticas
    de interacción de cada contenido.

    :param category_id: El ID de la categoría de la que se desean obtener los contenidos.
    :type category_id: int
    :return: Un diccionario JSON que representa información detallada de los contenidos de la categoría.
    :rtype: dict
    """
    categoria = Categoria.objects.get(id=category_id)
    contenidos = Contenido.objects.filter(subcategoria__categoria=categoria)

    interacciones_por_contenido = {}

    for contenido in contenidos:
        contenido_json = contenido_to_json(contenido)
        interacciones_por_contenido[contenido.id]=contenido_json

    return interacciones_por_contenido


def get_informacion_contenido(request, categoria_id):
    """
    Vista para obtener y devolver información detallada de contenidos de una categoría en formato JSON.

    Esta vista toma un ID de categoría y utiliza la función 'interacciones_categoria_json' para obtener información detallada
    de los contenidos pertenecientes a esa categoría en formato JSON. Luego, devuelve este JSON como respuesta a la solicitud.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :param categoria_id: El ID de la categoría de la que se desean obtener los contenidos.
    :type categoria_id: int
    :return: Una respuesta JSON que contiene información detallada de los contenidos de la categoría.
    :rtype: JsonResponse
    """
    return JsonResponse(interacciones_categoria_json(categoria_id))

@login_required
@has_permission_decorator('view_reports')
def mostrar_reportes_por_categoria(request,categoria_id):
    """
    Vista para mostrar reportes específicos de una categoría.

    Esta vista toma un ID de categoría y obtiene información de la categoría correspondiente. Luego, renderiza una página HTML
    de informes específicos para esa categoría, pasando la información de la categoría como contexto.

    :param request: La solicitud HTTP.
    :type request: HttpRequest
    :param categoria_id: El ID de la categoría para la que se mostrarán los informes.
    :type categoria_id: int
    :return: Una respuesta HTML que muestra los informes de la categoría.
    :rtype: HttpResponse
    """
    categoria = Categoria.objects.get(id=categoria_id)
    return render(request, 'reportes/reportes_por_categoria.html',{'category': categoria})
