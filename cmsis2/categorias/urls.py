from django.urls import path
from . import views

urlpatterns = [
    path('', views.categorias, name='categorias'),
    path('crear_categoria/', views.crear_categoria, name='crear_categoria'),
    path('mas_informacion_categoria/<int:categoria_id>', views.mas_informacion_categoria, name='mas_informacion_categoria'),
    path('editar_categoria/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('inactivar_rol/<int:categoria_id>/', views.inactivar_categoria, name='inactivar_categoria'),
    path('subcategorias/', views.subcategorias, name='subcategorias'),
    path('crear_subcategoria/', views.crear_subcategoria, name='crear_subcategoria'),
    path('mas_informacion_subcategoria/<int:subcategoria_id>', views.mas_informacion_subcategoria, name='mas_informacion_subcategoria'),
    path('editar_subcategoria/<int:subcategoria_id>/', views.editar_subcategoria, name='editar_subcategoria'),
    path('inactivar_subcategoria/<int:subcategoria_id>/', views.inactivar_subcategoria, name='inactivar_subcategoria'),
    path('agregar_usuario/<int:categoria_id>/', views.agregar_usuario, name='agregar_usuario'),
    path('quitar_usuario/<int:role_category_id>/', views.quitar_usuario, name='quitar_usuario'),
    path('ver_categoria/<int:categoria_id>/', views.ver_categoria, name='ver_categoria'),
    path('ver_subcategoria/<int:subcategoria_id>/', views.ver_subcategoria, name='ver_subcategoria'),
    path('kanban/<int:categoria_id>', views.mostrar_kanban, name='kanban'),
]