from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile
from orders.models import Order
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from carts.views import _cart_id # funcion que permitira  buscar si hay un carrito de compras
from carts.models import Cart, CartItem
import requests
# Create your views here.

def register(request):
    form = RegistrationForm() #instanciamiento
    if request.method == 'POST': #VALIDACION DEL ACTION DEL FORMULARIO
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0] #validacion del username asignandole el email
                                    #campo de la funcion = variable creada en el if
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            #215 creacion del perfil de usuario
            profile = UserProfile() 
            profile.user_id =user.id  #cuando se ejecuta el save , django genera un id para el objeto user, despues del metodo save, opodemos usar el id para enlazarlo con la clase profileen su propiedad user_id
            profile.profile_picture = 'default/default-user.png'
            profile.save()
            

            #proceso de activacion de cuenta
            current_site = get_current_site(request)
            mail_subject = 'Confirm your account'
            body = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), #cifrado de la clave primaria
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, body, to = [to_email])
            send_email.send()

            #messages.success(request, 'Register success')
            return redirect('/accounts/login/?command=verification&email='+email) #cuando ek usuario active el correo se devolvera la pagina de login con lo dos parametros, commando y el email, 
                                                                                    #se continua la validacion en el login
        
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email'] #valida las casillas
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password) #el metodo authenticate necesita los parametros email y password

        if user is not None: 
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation= item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    #  product_variation = [1, 2, 3, 4, 5]
                    #  ex_var_list = [5, 6, 7, 8]

                    for pr in product_variation:
                            if pr in ex_var_list:
                                index = ex_var_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity +=1
                                item.user = user
                                item.save()
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()
            except:
                pass
            
                #?next=/cart/checkout/
            auth.login (request, user)
            messages.success(request, 'Login succesfully')
            #capturar la url  de la linea 98
            url  = request.META.get('HTTP_REFERER')            
            #captura del parametro
            try:
                query = requests.utils.urlparse(url).query 
                #  ?next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect (nextPage)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'The username or password are incorrect')
            return redirect ('login')
        

    return render(request, 'accounts/login.html')

@login_required(login_url = 'login') #requiere que el login este activo
def logout(request):
    auth.logout(request)
    messages.success(request, 'Log out successfully')
    return redirect('login')

def activate(request, uidb64, token): #se activara cuando el usuario reciba el correo y active el link
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):  #si no es vacio
        user.is_active = True
        user.save()
        messages.success(request, 'Congrats, your account is verified')
        return redirect('login')
    else: #error en la activacion
        messages.error(request, 'Activation was not success')
        return redirect('register')

@login_required(login_url='login')#incluir la logica para obtener el numero de ordenes, #211
def dashboard(request):
    #hacer query
    orders = Order.objects.order_by('-created_at').filter(user_id= request.user.id, is_ordered=True) 
    orders_count = orders.count() #obtener la cantidad de ordenes
    #obtener el user profile    #217
    userprofile = UserProfile.objects.get(user_id = request.user.id) #obtener la informacion del perfil para poder hacer uso de los datos como la imagen de perfil
    context = {'orders_count' : orders_count, 'userprofile': userprofile,}
    return render(request, 'accounts/dashboard.html', context)

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']  #capturar el valor del email
        if Account.objects.filter(email = email).exists(): #validar si el email existe
            user = Account.objects.get(email__exact = email) #obtenemos el usuario de la bd
            #envio del email
            current_site = get_current_site(request)
            mail_subject = 'Restore password'
            body = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()

            messages.success(request, 'Check out to you inbox to reset your password')
            return redirect('login')
        else:
            messages.error(request, 'The username not exits')
            return redirect('forgotPassword')

    return render (request, 'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64, token): #procesara el link de reseteo 
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk = uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid # procesa el link 
        messages.success(request, 'Please, reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'The link is disabled')
        return  redirect ('login')
        
def resetPassword(request):
    if request.method == 'POST': # si el request es post entonces captura el valor del password del cliente
        password = request.POST['password'] #toma los valor del input del formulario
        confirm_password = request.POST['confirm_password']

        if password == confirm_password: #
            uid = request.session.get('uid') #capture el uid desde el request
            user = Account.objects.get(pk = uid) #captura del usuario
            user.set_password(password)
            user.save()
            messages.success(request, 'Password has been reset succesfully')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match ')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')
    
#crear la vista y obtener los datos de cada orden de compra,    #212
def my_orders(request):
    orders = Order.objects.filter(user = request.user, is_ordered =True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)

@login_required(login_url= 'login')
def edit_profile(request): #214
    userprofile = get_object_or_404(UserProfile, user = request.user) #consulta para obtener el perfil de usuario, obteniendo la entidad y cla condicion donde el user sea igual a request.user
    if request.method =='POST':  #evaluar y alamacenar actualizando la data del formulario de edit_profile
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Data saved successfully')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance = request.user)
        profile_form = UserProfileForm(instance = userprofile)
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required(login_url= 'login') #216
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact = request.user.username)  #buscar al usuario

        if new_password == confirm_password:
            success = user.check_password(current_password) #haccer una validacion con las condiciones de django
            if success:
                user.set_password(new_password)
                user.save()

                messages.success(request, 'Your password has changed')
                return redirect ('dashboard')
            else:
                messages.error(request, 'Please, enter a valid password')
                return redirect('change_password')
        else:
            messages.error(request, "Both password don't match")
            return redirect('change_password')
    
    return render (request, 'accounts/change_password.html')

