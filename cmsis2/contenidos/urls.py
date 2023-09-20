from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_contenido, name='crear_contenido'),
]