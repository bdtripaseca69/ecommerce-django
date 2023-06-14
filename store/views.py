from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

# Create your views here.
def store(request, category_slug=None):
    categories = None  #se condicionara la consulta dependiendo si esta consulta esta filtrada
    products = None
    if category_slug != None: #si es diferente la url, si no tiene parametros... se ejecutara si se envia el parametro de la categoria en la url
        #si encunetra la categoria se lista
        categories= get_object_or_404(Category, slug = category_slug) #funcion de django tipo exception, el slug representara un campo de la tabla categoria que estra haciendo la comparacion contra el parametro
        products = Product.objects.filter(category = categories, is_available = True)
        product_count = products.count() 
    else:
        products = Product.objects.all().filter(is_available = True)
        product_count = products.count() #cantidad de productos que hay en la db

    context = {'products': products,
            'product_count':product_count }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)#validar la categoria comparando con los datos del slug
        #en el html solo se utilizara esa variable para llamar a los campos de la tabla
    except Exception as e:
        raise e
    context = {'single_product': single_product,}
    return render(request, 'store/product_detail.html', context)
