from django import forms


#clase para construir el formulario instanciando un formulario de contacto

class FormularioContacto(forms.Form):
    name = forms.CharField(label="name", max_length=50, required=True)  #campos del tipico formulario de contacto
    email = forms.EmailField(label="email", required=True)
    message = forms.CharField( widget=forms.Textarea)

