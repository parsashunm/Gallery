from django.contrib import admin
#
from .models import (
    Product, ProductsImage, Auction, AuctionProduct,
)
#
admin.site.register(Auction)
#


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', 'price']


@admin.register(ProductsImage)
class ProductsImageAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(AuctionProduct)
class AuctionProductsAdmin(admin.ModelAdmin):
    fieldsets = [
        (' ', {
            'fields':
            [
                'auction',
                'product',
                'base_price',
                'minimum_bid_increment',
            ]
        })
    ]
