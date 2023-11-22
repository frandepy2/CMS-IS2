from django.urls import path
from . import views


urlpatterns = [
    path('<int:usuario_id>/', views.obtener_notificaciones, name='obtener_notificaciones'),
]