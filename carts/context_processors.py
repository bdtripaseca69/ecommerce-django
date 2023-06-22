#referencia para que el icono del carrito identifique cuantos items tiene agregados
from .models import Cart, CartItem
from .views import _cart_id  #permite usar la funcion que permite buscar el carrito de compras con el parametro request

def counter(request): #funcion global
    cart_count = 0
    try: 
        cart = Cart.objects.filter(cart_id = _cart_id(request))  #buscar el carrito

        if request.user.is_authenticated:
            cart_items = CartItem.objects.all().filter(user=request.user) #la busqueda de los items se llevara a cabo por el parametro de user,todos los items registrados seran devueltos
        else:
            cart_items = CartItem.objects.all().filter(cart = cart[:1]) #condicion para traer  un elemento a la busqued del filter
        
        for cart_item in cart_items:    #evalua la cantidad de productos que tiene el carrito
            cart_count += cart_item.quantity
    except Cart.DoesNotExist:
        cart_count = 0
    return dict(cart_count = cart_count)
