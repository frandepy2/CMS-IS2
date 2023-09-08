from django.urls import path
from . import views

urlpatterns = [
    path('',views.roles, name='roles'),
    path('crear_rol/', views.crear_rol, name='crear_rol'),
    path('mas_informacion/<int:role_id>', views.mas_informacion_rol, name='mas_informacion_rol'),
    path('editar_rol/<int:role_id>/', views.editar_rol, name='editar_rol'),
    path('inactivar_rol/<int:role_id>/', views.inactivar_rol, name='inactivar_rol'),
]