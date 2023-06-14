from django.contrib import admin
from .models import Category
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)} #en esta sentencia se hace que el slug se autocomplete en el panel admin
    list_display = ('category_name', 'slug')


admin.site.register(Category, CategoryAdmin)