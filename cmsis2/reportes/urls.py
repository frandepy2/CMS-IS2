from django.urls import path
from . import views


urlpatterns = [
    path('', views.mostrar_reportes, name='mostrar_reportes'),
]