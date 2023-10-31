from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from categorias.models import Categoria, Subcategoria #TODO quitar cmsis2
from interacciones.models import Accion #TODO quitar cmsis2
from contenidos.models import Contenido #TODO quitar cmsis2
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image,Paragraph,Spacer,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import matplotlib.pyplot as plt


# Create your views here.
def mostrar_reportes(request):
    return render(request, 'reportes/reportes.html')

def calcular_interacciones_por_categoria():
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
    interacciones = calcular_interacciones_por_categoria()
    return JsonResponse(interacciones)


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

def generar_pdf(request):
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


#Cantidad de likes de los contenidos en una categoria

#Cantidad de compentarios  de los  contenidos en una categoria

#Cantidad de compartir  de los  contenidos en una categoria

#Cantidad de denuncias de los contenidos en una categoria

#generar_pdf_de_categoria