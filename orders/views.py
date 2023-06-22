from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms  import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse #200
# Create your views here.

def payments(request):
    body = json.loads(request.body)#capturara todos los valores que se encuentran en el body del codigo jS    
    order = Order.objects.get(user = request.user, is_ordered=False, order_number = body['orderID'])

    #creacion del objeto payment
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_id = order.order_total,
        status = body ['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered=True
    order.save()

    #mover de carrito items y registrar en la tabla order product todo el carrito
    cart_items =CartItem.objects.filter(user = request.user)
    for item in cart_items: #insert
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True  
        orderproduct.save()

        cart_item = CartItem.objects.get(id= item.id) #buscar al cartItem por el id
        product_variation = cart_item.variations.all() #buscar la variation del producto
        orderproduct = OrderProduct.objects.get(id = orderproduct.id) # buscar al orderproducto, reiniciandolo 
        orderproduct.variation.set(product_variation) #
        orderproduct.save()

        #video 198, actualizar stock y redireccionar templates despues del pago
        product = Product.objects.get(id = item.product_id)
        product.stock -= item.quantity #decrementa dependiendo de la cantidad comprada
        orderproduct.save()

        #borrar carrito despues de la compra
    CartItem.objects.filter(user = request.user).delete()


        #envio de correo al cliente con los datos de la compra
    mail_subject = 'Thanks for your purchase'
    body = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, body, to=[to_email])
    send_email.send()

    data = {
        'order_number': order.order_number,
        'transID' : payment.payment_id,
    }

    return JsonResponse(data) # 200, obtiene los datos js desde el template payments


def place_order(request, total = 0, quantity = 0): #captura de los items del carrito
    current_user = request.user
    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)#multiplicando el; precio del prodicto por la cantidad de productos 
        quantity += cart_item.quantity
    
    tax = (2* total)/100
    grand_total = total + tax

    #agregado de los datos del clien
    if request.method == 'POST':
        form = OrderForm(request.POST) #enlazado de los datos que se definiran con los atributos del formuilario
        if form.is_valid():
            data = Order()
            data.user = current_user #datos de la sesion 
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.addres_line_1 = form.cleaned_data['addres_line_1']
            data.addres_line_2 = form.cleaned_data['addres_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.date.today().strftime('%Y')) #sentencia para obtener el ano, 
            mt = int(datetime.date.today().strftime('%m')) #mes
            dt = int(datetime.date.today().strftime('%d')) #dia
            d = datetime.date (yr, mt, dt)
            #formato de la fecha para generar parte del numero de compra
            current_date = d.strftime("%Y%m%d")
            order_number = current_date +str(data.id)
            data.order_number = order_number
            data.save()

            #datos a enviar al payments.html
            order = Order.objects.get(user = current_user, is_ordered = False, order_number = order_number)#parametros que se necesitan para filtrar y obtener el objeto desde la base de datos
            context = {
                'order': order,
                'cart_items': cart_items,
                'total' : total,
                'tax': tax,
                'grand_total': grand_total,
            }

            return render(request, 'orders/payments.html', context)
    else:
        return redirect ('checkout')
    
def order_complete(request): #200, confirmacion de compra
    #201
    order_number = request.GET.get('order_number')  #captura de parametros que envia el cliente por la url para la ejecucion de order_complete
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True) #busqueda desde la base de datos
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products: #actualizacion del precio, lee cada producto ordenado
            subtotal += i.product_price*i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('Home')
        
