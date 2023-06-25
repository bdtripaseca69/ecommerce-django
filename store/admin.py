from django.contrib import admin
from .models import Product, ReviewRating, ProductGallery 
import admin_thumbnails # 226
# Register your models here.

#agregar una lista con las imagenes del producto -- #226
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug':('product_name',)}
    search_fields = ('product_name', "marca", 'category')   #casilla de busqueda segun el criterio
    list_filter = ('product_name', "marca", 'category')
    inlines=[ProductGalleryInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery) #226