from django.shortcuts import render
from django.http import JsonResponse
from categorias.models import Categoria, Subcategoria
from interacciones.models import Accion
from contenidos.models import Contenido
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image,Paragraph
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
    # Obtén los datos que deseas incluir en el PDF, por ejemplo, interacciones_por_categoria
    datos = calcular_interacciones_por_categoria()  # Reemplaza con tus datos reales

    # Crear un objeto de BytesIO para almacenar el PDF en memoria
    buffer = BytesIO()

    # Crear un documento PDF con ReportLab
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Definir estilos para el título y subtítulo
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    subtitle_style = styles['Heading1']

    # Agregar título y subtítulo
    title = Paragraph("Reporte del sistema", title_style)
    subtitle = Paragraph("Cantidad de likes de cada Categoria", subtitle_style)

    # Generar el gráfico con Matplotlib
    plt.figure(figsize=(8, 4))
    categorias = list(datos.keys())

    # Ordenar las fechas
    fechas = sorted(list(datos[categorias[0]].keys()))

    # Crear una lista para almacenar los valores de cada categoría
    valores_por_categoria = []

    for categoria in categorias:
        valores = []
        for fecha in fechas:
            valor = datos[categoria].get(fecha, 0)
            valores.append(valor)
        valores_por_categoria.append(valores)
        plt.plot(fechas, valores, marker='o', linestyle='-', label=categoria)

    plt.xlabel('Fechas')
    plt.ylabel('Interacciones')
    plt.title('Interacciones por Fecha')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    # Guardar el gráfico en un objeto de BytesIO
    image_buffer = BytesIO()
    plt.savefig(image_buffer, format='png')
    plt.close()
    image_buffer.seek(0)

    # Crear una imagen con el gráfico usando ReportLab
    image = Image(image_buffer, width=400, height=200)

    # Crear una tabla para mostrar los datos
    table_data = [["Categoría"] + fechas] + [[categoria] + valores for categoria, valores in zip(categorias, valores_por_categoria)]

    t = Table(table_data, repeatRows=1)

    # Estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    t.setStyle(style)

    # Construir el PDF
    elements = [title, subtitle, image, t]
    doc.build(elements)

    # Obtener el contenido del PDF y cerrar los objetos de BytesIO
    pdf = buffer.getvalue()
    buffer.close()
    image_buffer.close()

    # Crear una respuesta HTTP con el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informe.pdf"'
    response.write(pdf)

    return response