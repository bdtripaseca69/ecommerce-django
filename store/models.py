from django.db import models 
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count #208
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
    
    #208 crear la funcion del promedio
    def averageReview(self):                                                #funcion que obtendra el promedio desde el rating
        reviews = ReviewRating.objects.filter(product = self, status = True).aggregate(average = Avg('rating')) #obtener el objeto review 
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    #209 para saber la cantidad de reviews
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
            return count





class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def tallas(self):
        return super(VariationManager, self).filter(variation_category='talla', is_active=True)


variation_category_choice = (
    ('color', 'color'),
    ('talla', 'talla'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return  self.variation_category + ' : ' +self.variation_value

class ReviewRating(models.Model): #202 creacion del modelo de review
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, blank=True)
    review = models.CharField(max_length=500, blank= True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.subject
    
class ProductGallery(models.Model):  #223
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self) -> str:
        return self.product.product_name


