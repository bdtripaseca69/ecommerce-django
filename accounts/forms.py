from django import forms
from .models import Account, UserProfile

#clase para construir el formulario instanciando un formulario de contacto
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password', 
        'class': 'form-control',
        }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password', 
        'class': 'form-control',
        }))
    class Meta:
        model = Account #se basara en la clase account y guarda la estructura del usuario
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'password') #este dato se envia en el views.py
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()  #instanciamiento
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        
#214 actualizar perfil de usuario
class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid': ('Image file only')}, widget=forms.FileInput) #atributo para el campo de imagen de perfil
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

