from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.

def _cart_id(request): #funcion provada
    cart = request.session.session_key #
    if not cart:#si no existe
        cart = request.session.create() #para crear una nueva sesion si no hay un carrito
    return cart

def add_cart(request, product_id): #buscar el elemento en la db, para crear el carrito
    product = Product.objects.get(id = product_id)
    current_user = request.user #saber si el usuario esta en sesion
    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        #record que representa el elemento seleccionado que se mostrara en el carro
        if is_cart_item_exists:
            #try:
            cart_item= CartItem.objects.get(product = product, user=current_user)  #busque por el producto y otro por el carrito, esto debido a los usuarios
            cart_item.quantity += 1 #instuccion para que cada que se agrege un item la cantidad aumente
            cart_item.save() 
            #except CartItem.DoesNotExist:
        else:
            cart_item = CartItem.objects.create(product = product, quantity = 1, user = current_user,)
            cart_item.save()
        return redirect ('cart')   

    else:
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
                ) #el parametro es para buscar el car a nivel local si existe o no
        
        cart.save()
        #record que representa el elemento seleccionado que se mostrara en el carro
        try:
            cart_item= CartItem.objects.get(product = product, cart=cart)  #busque por el producto y otro por el carrito, esto debido a los usuarios
            cart_item.quantity += 1 #instuccion para que cada que se agrege un item la cantidad aumente
            cart_item.save() 
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product = product, quantity = 1, cart = cart,)
            cart_item.save()
        return redirect ('cart')   

    
    

def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id) #encontrar cart_item
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

    cart_item.delete()
    return redirect('cart')


def cart(request, total = 0, quantity = 0, cart_items = None):
    tax = 0
    grand_total = 0
    #consultas de la db
    try:
        if request.user.is_authenticated: #valida que exista una sesion para mantener el item dentro del carrito
            cart_items = CartItem.objects.filter(user = request.user, is_active = True)
        else:   
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart = cart, is_active = True)
        
        for cart_item in cart_items: #para poder saber el precio total yy la cantidad
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2* total)/100
        grand_total = total + tax
        
    except ObjectDoesNotExist:
        pass

    context = {'total': total, 
            'quantity': quantity, 
            'cart_items': cart_items, 
            'tax': tax, 
            'grand_total': grand_total,
            }
    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request, total = 0, quantity = 0, cart_items = None):
    tax = 0
    grand_total = 0
    #consultas de la db
    try:
        
        if request.user.is_authenticated: #valida que exista una sesion para mantener el item dentro del carrito
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            
        for cart_item in cart_items: #para poder saber el precio total yy la cantidad
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2* total)/100
        grand_total = total + tax
        
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total, 
        'quantity': quantity, 
        'cart_items': cart_items, 
        'tax': tax, 
        'grand_total': grand_total,
    }
    
    return render(request, 'store/checkout.html',context)