from django.urls import path
from . import views

urlpatterns = [
    path('',views.categorias, name='categorias'),
    path('crear_categoria/', views.crear_categoria, name='crear_categoria'),
    path('mas_informacion_categoria/<int:categoria_id>', views.mas_informacion_categoria, name='mas_informacion_categoria'),
    path('editar_categoria/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('inactivar_rol/<int:categoria_id>/', views.inactivar_categoria, name='inactivar_categoria'),
    path('subcategorias/', views.subcategorias, name='subcategorias'),
    path('crear_subcategoria/', views.crear_subcategoria, name='crear_subcategoria'),
    path('mas_informacion_subcategoria/<int:subcategoria_id>', views.mas_informacion_subcategoria, name='mas_informacion_subcategoria'),
    path('editar_subcategoria/<int:subcategoria_id>/', views.editar_subcategoria, name='editar_subcategoria'),
    path('inactivar_subcategoria/<int:subcategoria_id>/', views.inactivar_subcategoria, name='inactivar_subcategoria'),
]