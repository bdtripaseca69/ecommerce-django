from django.contrib import admin
from .models import Product, ReviewRating
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug':('product_name',)}
    search_fields = ('product_name', "marca", 'category')   #casilla de busqueda segun el criterio
    list_filter = ('product_name', "marca", 'category')

admin.site.register(Product, ProductAdmin)
admin.site.register(ReviewRating)