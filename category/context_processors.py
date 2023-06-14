from .models import Category
from store.models import Product

def menu_links(request):
    links = Category.objects.all()
    product_link = Product.objects.all()
    return dict(links = links, product_link = product_link)
