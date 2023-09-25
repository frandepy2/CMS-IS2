from django.urls import path
from . import views

urlpatterns = [
    path('plantillas/', views.seleccionar_plantilla, name='seleccionar_plantilla'),
    path('plantillas/previsualizar/<int:plantilla_id>', views.previsualizar, name='previzualizar'),
]
