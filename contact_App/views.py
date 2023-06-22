from django.shortcuts import render, redirect
#from contact_App.models import  
from .forms import FormularioContacto
# Create your views here.
from django.core.mail import EmailMessage #para mandar los correos

def contact_view(request):
    formulario_contacto= FormularioContacto()
    if request.method == "POST":
        formulario_contacto = FormularioContacto(data=request.POST) #cargar la info del formulario y pasar el parametro de los datos al constructor
        if formulario_contacto.is_valid():
            name = request.POST.get("name")
            email = request.POST.get("email")
            message = request.POST.get("message")
            infForm= formulario_contacto.cleaned_data                                                                       #quien lo recibe, en settings.py es quien lo envia
            email = EmailMessage("message from store", "User: {} \n Email: {}\n Message: {}".format(name,email,message),"",["ing.martinezbd@gmail.com"], reply_to=[email])
            
            try:
                email.send()
                return redirect("/contact/?valid") #manda un get
            #redirecciona despues del metodo post un parametro a la url validando el envio del post
            except:
                return redirect("/contact/?Novalid")
        else:
            formulario_contacto = FormularioContacto() #vacio debido a que no ha ingresado informacion
    

    return render(request, 'includes/contact.html', {"miformulario": formulario_contacto})

