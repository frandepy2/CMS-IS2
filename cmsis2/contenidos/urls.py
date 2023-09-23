from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_contenido, name='crear_contenido'),
    path('ver/<int:contenido_id>/', views.ver_contenido, name='ver_contenido'),
    path('preview/<int:contenido_id>/', views.preview_contenido, name='preview_contenido'),
    path('editar/<int:contenido_id>/', views.editar_contenido, name='editar_contenido'),
]