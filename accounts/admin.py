from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin #modulo para la modificacion del panel
# Register your models here.
#condiciones para
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active') #propiedades para mostrar informacion
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('date_joined',) #que se organice ascendentemente
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



admin.site.register(Account, AccountAdmin)