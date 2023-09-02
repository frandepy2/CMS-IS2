from django.urls import path, include

from . import views

urlpatterns = [
    path('',views.usuarios, name='usuarios'),
    path('manage/<int:user_id>/',views.manage_user, name='manage_user'),
]