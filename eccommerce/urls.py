"""
URL configuration for eccommerce project.

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
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('securelogin/', admin.site.urls), #219 se complementa con el honeypot, para la creacion de un fack admin adminstrator, complementar en setting.py
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')), #para evitar issues se uso esta alternativa: pip install django-admin-honeypot-updated-2021==1.2.0
    path('', views.home, name='Home'),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('contact/', include('contact_App.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #indica que la url de los archivos media se le agrege las rutas que siguen a /media

