from django.urls import path
from . import views

urlpatterns = [
    path('ver/<int:contenido_id>/', views.ver_contenido, name='ver_contenido'),
    path('editar/<int:contenido_id>/', views.editar_contenido, name='editar_contenido'),
    path('gestionar/', views.gest_contenidos, name='gest_contenidos'),
    path('gestionar/borrador/', views.ver_borrador, name='contenidos_borrador'),
    path('gestionar/revision/', views.ver_revision, name='contenidos_revision'),
    path('gestionar/edicion/', views.ver_edicion, name='contenidos_edicion'),
    path('gestionar/rechazados/', views.ver_rechazados, name='contenidos_rechazados'),
    path('gestionar/inactivos/', views.ver_inactivos, name='contenidos_inactivos'),
    path('gestionar/publicados/', views.ver_publicados, name='contenidos_publicados'),
    path('aprobar_contenido/<int:contenido_id>/', views.aprobar_contenido, name='aprobar_contenido'),
    path('rechazar_contenido/<int:contenido_id>/', views.rechazar_contenido, name='rechazar_contenido'),
    path('enviar_edicion/<int:contenido_id>/', views.enviar_edicion, name='enviar_edicion'),
    path('enviar_revision/<int:contenido_id>/', views.enviar_revision, name='enviar_revision'),
    path('plantillas/<int:categoria_id>', views.seleccionar_plantilla, name='seleccionar_plantilla'),
    path('plantillas/previsualizar/<int:plantilla_id>', views.previsualizar, name='previzualizar'),
    path('crear/plantilla/<int:plantilla_id>/<int:categoria_id>', views.crear_contenido, name='crear_contenido'),
    path('denunciar/<int:contenido_id>', views.denunciar_contenido, name='denunciar_contenido')
]
