from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_contenido, name='crear_contenido'),
    path('ver/<int:contenido_id>/', views.ver_contenido, name='ver_contenido'),
    path('preview/<int:contenido_id>/', views.preview_contenido, name='preview_contenido'),
    path('editar/<int:contenido_id>/', views.editar_contenido, name='editar_contenido'),
    path('gestionar/', views.gest_contenidos, name='gest_contenidos'),
    path('gestionar/borrador/', views.ver_borrador, name='contenidos_borrador'),
    path('gestionar/revision/', views.ver_revision, name='contenidos_revision'),
    path('gestionar/rechazados/', views.ver_rechazados, name='contenidos_rechazados'),
    path('gestionar/inactivos/', views.ver_inactivos, name='contenidos_inactivos'),
]