from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

#
from .models import (
    Product, ProductsImage, Auction, AuctionProduct, Category, Attribute, AttributeValue, ProductAttributeValue
)
#
admin.site.register(Auction)
admin.site.register(AuctionProduct)
#


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ['value', 'id']


class AttributeValueInLine(admin.TabularInline):
    model = AttributeValue
    extra = 0


class ProductAttributeValueInLine(admin.TabularInline):
    model = ProductAttributeValue
    extra = 0


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    inlines = [AttributeValueInLine]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', 'price']
    inlines = [ProductAttributeValueInLine]


@admin.register(ProductsImage)
class ProductsImageAdmin(admin.ModelAdmin):
    list_display = ['id']


# @admin.register(AuctionProduct)
# class AuctionProductsAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (' ', {
#             'fields':
#             [
#                 'auction',
#                 'product',
#                 'base_price',
#                 'minimum_bid_increment',
#                 'is_presenting',
#             ]
#         })
#     ]


class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)
    list_display = ['title', 'id']


admin.site.register(Category, CategoryAdmin)
