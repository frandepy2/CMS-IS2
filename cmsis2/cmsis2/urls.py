"""
URL configuration for cmsis2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import HomeView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('socialaccount/', include('allauth.urls')),
    path('usuarios/', include("usuarios.urls")),
    path('roles/', include("roles.urls")),
    path('categorias/', include("categorias.urls")),
    path('contenidos/', include("contenidos.urls")),
    path('parametros/', include("parametros.urls")),
    path('interacciones/', include('interacciones.urls')),
    path('reportes/', include('reportes.urls')),
    path('notificaciones/', include('notificaciones.urls')),
    path('', HomeView, name='home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
