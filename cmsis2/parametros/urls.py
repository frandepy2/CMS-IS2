from django.urls import path
from . import views

urlpatterns = [
    path('parametros/', views.lista_y_editar_parametros, name='lista_y_editar_parametros'),
    path('parametros/editar/<int:parametro_id>/', views.lista_y_editar_parametros, name='editar_parametro'),
]