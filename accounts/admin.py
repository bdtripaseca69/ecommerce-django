from django.contrib import admin
from .models import Account, UserProfile
from django.contrib.auth.admin import UserAdmin #modulo para la modificacion del panel
from django.utils.html import format_html
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

class UserProfileAdmin(admin.ModelAdmin):  #213
    def thumbnail(self, object): #definir un control para el manejo de imagenes
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile  picture'
    list_display= ('thumbnail', 'user', 'city', 'state', 'country')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Account, AccountAdmin)