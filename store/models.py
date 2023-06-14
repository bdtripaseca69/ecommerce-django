from django.db import models 
from category.models import Category
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length = 100, unique = True)
    slug = models.CharField(max_length = 200, unique = True)
    descripcion = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    imagenProduct = models.ImageField(upload_to="photos/products")
    imagenSPECS = models.ImageField(blank=True, upload_to="photos/products")
    stock = models.IntegerField()
    marca = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)
    category= models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    class Meta: #representacion en la db, encontrara el modelo(tabla) segun la informacion proporcionada
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def get_url(self):  #product_detail es el del url mas la vista con los parametros slug de la vista y el slug del producto
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self) -> str:
        return self.product_name  