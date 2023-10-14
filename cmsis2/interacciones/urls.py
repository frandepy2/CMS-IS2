from django.urls import path
from . import views

urlpatterns = [
    path('crear_comentario/<int:contenido_id>', views.crear_comentario, name='crear_comentario'),
]