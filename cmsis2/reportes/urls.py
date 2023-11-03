from django.urls import path
from . import views


urlpatterns = [
    path('', views.mostrar_reportes, name='mostrar_reportes'),
    path('category/interactions',views.interacciones_por_categoria, name='interacciones_por_categoria'),
    path('category/reports',views.reportes_por_categoria,name= 'reportes_por_categoria'),
    path('category/dateviews',views.visualizaciones_por_categoria_por_fecha, name='visualizaciones_por_categoria_por_fecha'),
    path('category/datelikes',views.likes_por_categoria_por_fecha, name='likes_por_categoria_por_fecha'),
    path('generar_pdf/', views.generar_pdf, name='generar_pdf'),
    path('category/<int:categoria_id>/obtener_informacion/', views.get_informacion_contenido, name='get_informacion_contenido'),
    path('categoria/<int:categoria_id>/', views.mostrar_reportes_por_categoria, name='mostrar_reportes_por_categoria')
]