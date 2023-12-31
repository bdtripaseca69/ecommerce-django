from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager #modelos para modificar la tabla raiz de django

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password = None):
        if not email:
            raise ValueError('User has not email')
        if not username:
            raise ValueError('User has not username')
        
        user = self.model(   #si las condiciones no se cumplen se ejecuta las definiciones de objetos user
            email = self.normalize_email(email), # 
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, username, password): #permite crear un superuser
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password= password,
            first_name= first_name,
            last_name= last_name,
        ) #crear el objeto user
        user.is_admin = True    #darle atributos de admin
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100 , unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    #campos y atributos de django
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' #permitira el login al panel con el email
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager() #instanciamiento

    #207 para mostrar een las reviews el nombre completo del usuario
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj = None): #solo si es admin podra hacer mdificaciones
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    
    #continuar en settings.py para especificar que estas clases sean las principales para el guardado de la info de los usuarios

class UserProfile(models.Model): #213, creacion de campos para el template edit profile
    user = models.OneToOneField(Account, on_delete=models.CASCADE) #tiene uan relacion 1 a 1 con Account  class
    address_line_1 = models.CharField(blank=True, max_length=150)
    address_line_2 = models.CharField(blank=True, max_length=150)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile/')
    city = models.CharField(blank=True, max_length=50)
    state = models.CharField(blank=True, max_length=50)
    country = models.CharField(blank=True, max_length=50)

    def __str__(self) -> str:
        return self.user.first_name
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
