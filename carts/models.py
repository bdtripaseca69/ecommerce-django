from django.db import models
from store.models import Product, Variation
from accounts.models import Account
# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=300, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null= True)  #comienza la relacion del carrito al user
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    variations = models.ManyToManyField(Variation, blank=True)


    def sub_total(self):
        return self.product.price * self.quantity 

    def __unicode__(self):
        return self.product