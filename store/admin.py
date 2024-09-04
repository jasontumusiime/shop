from django.contrib import admin

from .models import Product, Variation


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


class VariationAdmin(admin.ModelAdmin):
  list_display = ('product', 'category', 'value', 'is_active', 'created_at')
  list_editable = ('category', 'is_active', )
  list_filter = ('product', 'category', 'value', 'is_active',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)