from django.urls import path, include

from . import views

urlpatterns = [
    path('',views.usuarios, name='usuarios'),
    path('manage/<int:user_id>/',views.manage_user, name='manage_user'),
    path('manage/<int:user_id>/asign/',views.asignar_rol, name='asignar_rol_usuario')
]