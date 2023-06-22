
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.contact_view, name="contact"),
] 

#urls dependeran del archivo urls.py del directorio general del proyecto

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #indica que la url de los archivos media se le agrege las rutas que siguen a /media