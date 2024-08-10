from django.contrib import admin

from .models import Product


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
  prepopulated_fields = { 'slug': ('name',),}
  list_display = (
    'name',
    'slug',
    'price',
    'image',
    'stock',
    'modified_at',
    'is_available',
  )



admin.site.register(Product, ProductAdmin)