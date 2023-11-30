from django.urls import path
from . import views


urlpatterns = [
    path('<int:usuario_id>/', views.obtener_notificaciones, name='obtener_notificaciones'),
    path('read/<int:notificacion_id>/', views.leer_notificacion, name='leer_notificacion'),
    path('ver_notificaciones', views.ver_todas, name='ver_notificaciones')
]