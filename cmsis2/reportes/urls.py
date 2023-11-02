from django.urls import path
from . import views


urlpatterns = [
    path('', views.mostrar_reportes, name='mostrar_reportes'),
    path('category/interactions',views.interacciones_por_categoria, name='interacciones_por_categoria'),
    path('category/reports',views.reportes_por_categoria,name= 'reportes_por_categoria'),
    path('category/dateviews',views.visualizaciones_por_categoria_por_fecha, name='visualizaciones_por_categoria_por_fecha'),
    path('category/datelikes',views.likes_por_categoria_por_fecha, name='likes_por_categoria_por_fecha'),
    path('generar_pdf/', views.generar_pdf, name='generar_pdf'),
    path('category/<int:category_id>/reports/', views.category_reports, name='category_reports'),
    path('generate_category_pdf/<int:category_id>/', views.generate_category_pdf, name='generate_category_pdf'),

    #'/categoria/<id_categoria>'
]