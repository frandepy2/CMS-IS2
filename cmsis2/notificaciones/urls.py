from django.urls import path
from . import views


urlpatterns = [
    path('<int:usuario_id>/', views.obtener_notificaciones, name='obtener_notificaciones'),
    path('read/<int:notificacion_id>/',views.marcar_como_leido, name='marcar_como_leido'),
]