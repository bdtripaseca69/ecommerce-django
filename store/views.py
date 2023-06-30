from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator #librerias que permite la paginacion
from django.db.models import Q #libreria para el apoyo en el uso de los campos search
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
from django.contrib import messages

# Create your views here.
def store(request, category_slug=None):
    categories = None  #se condicionara la consulta dependiendo si esta consulta esta filtrada
    products = None
    if category_slug != None: #si es diferente la url, si no tiene parametros... se ejecutara si se envia el parametro de la categoria en la url
        #si encunetra la categoria se lista
        categories= get_object_or_404(Category, slug = category_slug) #funcion de django tipo exception, el slug representara un campo de la tabla categoria que estra haciendo la comparacion contra el parametro
        products = Product.objects.filter(category = categories, is_available = True).order_by('-id')
        
        paginator = Paginator(products, 6) #se vuelven a colocar las mismas sentencias para que se tome en cuenta los filtros de las categorias 
        page = request.GET.get('page')  
        paged_products = paginator.get_page(page) 
        
        product_count = products.count() 
        
    else:
        products = Product.objects.all().filter(is_available = True).order_by('-id')
        paginator = Paginator(products, 6)  #llamar a una instancia del paginator... dos parametros; grupo o colecion a paginar, y el grupo de cuantos objetos mostrar
        page = request.GET.get('page')  #acceso a dichas paginas, mediante la captura de los urls como parametro de la url a acceder
        paged_products = paginator.get_page(page) #indicar a donde envie la lista de paginas, representara solo 5 items
        product_count = products.count() #cantidad de productos que hay en la db

    context = {'products': paged_products,
            'product_count':product_count }
    
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)#validar la categoria comparando con los datos del slug
        #en el html solo se utilizara esa variable para llamar a los campos de la tabla
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product = single_product).exists() #consulta para saber si ya hay un carrito con ese item. si existe un record sera true
    except Exception as e:
        raise e
    #210 condicionar si hay o no sesion
    if request.user.is_authenticated:
        # 206 validar quee el usuario este logeado
        try:
            orderproduct = OrderProduct.objects.filter(user = request.user, product_id = single_product.id).exists() #si existe en el orderproduct significa que ya se compro
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    #207  mostrar la lista de reviews
    reviews = ReviewRating.objects.filter(product_id = single_product.id, status = True) #devuelve la collecion de reviews

    #227 #filtrado del producto por el id para mostrar las imagenes, se complementa con jquery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews' : reviews,
        'product_gallery': product_gallery,
        }
    return render(request, 'store/product_detail.html', context)



def search(request):
    if 'keyword' in request.GET: # saber si se recibe el url la palabra keyword
        keyword = request.GET['keyword'] #obener el parametro desde la url
        if keyword:
            # consulta para obtener el conjunto de productos que corresponden a la busqueda
                            #ordenamiento por la fecha de creacion, descendiente
            products = Product.objects.order_by('-created_date').filter(Q(descripcion__icontains = keyword) | Q(product_name__icontains = keyword))  #query el keyword se comparara con el campo product_name y descripcion de la tabla producto
            product_count = products.count()
        else:
            messages.error(request, "Write anything else")
            return redirect('Home')

    context = {
        'products': products,
        'product_count':product_count,
    }
    return render(request, 'store/store.html', context)

def submit_review(request, product_id):  #205
    url = request.META.get('HTTP_REFERER') #captura del url
    if request.method == 'POST':      #parametrso del request post
        try: #capturar todos los objetos review
            reviews = ReviewRating.objects.get(user__id = request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews) #instancia del form
            form.save()
            messages.success(request, 'Your review has been updated') #review encontrado y actualizandolo
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Your review has been sent') #review  NO encontrado y creado
                return redirect(url)