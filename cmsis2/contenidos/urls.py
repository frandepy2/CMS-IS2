from django.urls import path
from . import views

urlpatterns = [
    path('plantillas/<int:categoria_id>', views.seleccionar_plantilla, name='seleccionar_plantilla'),
    path('plantillas/previsualizar/<int:plantilla_id>', views.previsualizar, name='previzualizar'),
    path('crear/plantilla/<int:plantilla_id>/<int:categoria_id>', views.crear_contenido, name='crear_contenido')
]
