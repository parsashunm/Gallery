from django.contrib import admin
#
from .models import Product, ProductsImage

admin.site.register(ProductsImage)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', 'price']
