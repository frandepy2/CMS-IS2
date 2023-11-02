from django.urls import path
from . import views

urlpatterns = [
    path('crear_comentario/<int:contenido_id>', views.crear_comentario, name='crear_comentario'),
    path('me_gusta/<int:contenido_id>', views.dar_me_gusta, name='dar_me_gusta'),
    path('compartir/<int:contenido_id>',views.compartir_contenido, name='compartir_contenido'),
]