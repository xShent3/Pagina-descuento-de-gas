"""
URL configuration for gas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from gas_licuado import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('crear/', views.crear_solicitud, name='crear_solicitud'),
    path('listar/', views.listar_solicitudes, name='listar_solicitudes'),
    path('buscar/', views.buscar_solicitud, name='buscar_solicitud'),
    path('detalle/<int:id>/', views.request_detail, name='request_detail'),
    path('eliminar/<int:id>/', views.delete_request, name='delete_request'),
    path('cambiar_estado/<int:id>/', views.cambiar_estado, name='cambiar_estado'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('ver_perfil/<int:id>/', views.ver_perfil, name='ver_perfil'),
    path('cambiar_contrasena/<int:id>/', views.cambiar_contrasena, name='cambiar_contrasena'),
    path('confirm_delete_user/<int:id>/', views.confirm_delete_user, name='confirm_delete_user'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
]
