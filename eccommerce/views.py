from django.shortcuts import render
from store.models import Product,  ReviewRating


def home(request):                                               #218, ultima instruccion para que se filtre por la fecha de creacion
    products = Product.objects.all().filter(is_available = True).order_by('created_date') #condicion para que liste solo los que estan disponibles
    
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status = True)


    context = {'products': products, 'reviews': reviews,}
    
    return render( request, 'home.html', context)
