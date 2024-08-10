from django.contrib import admin
#
from .models import Product, ProductsImage
#
# register simper models here
#


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', 'price']


@admin.register(ProductsImage)
class ProductsImageAdmin(admin.ModelAdmin):
    list_display = ['id']
