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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'), #path actualizado para las funciones del input search
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'), #url para mandar al detail.html
    path('search/', views.search, name='search'), #path del search
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'), #path para el review #205
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #indica que la url de los archivos media se le agrege las rutas que siguen a /media

