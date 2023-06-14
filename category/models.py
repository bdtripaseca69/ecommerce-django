from django.db import models
from django.urls import reverse
# Create your models here.
class Category (models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=300, blank= True) #blank es para que acepte valores nulos
    slug = models.CharField(max_length=100, unique=True) #es un valor que se utiliza para estar en la parte final de las url que representa a un parametro
    

    class Meta:
        verbose_name= 'category' #sentencias para que en el panel de administracion la tabla no sea modificada con el plural
        verbose_name_plural = 'categories'
    
    def get_url(self): #funcion para que tome los valores del slug y permita que la lista de categorias filtre el contenido
        return reverse('products_by_category', args = [self.slug]) #nombre del url de la appstore, argumento slug representando el objeto categoria
    
    def __str__(self): #sentencias para que la info sea mostrada en el admin
        return self.category_name
