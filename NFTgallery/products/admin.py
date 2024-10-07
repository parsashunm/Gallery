from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from django.contrib import messages
from utils import calculate_product_profit
#
from .models import (
    Product, ProductsImage, Auction, AuctionProduct, Category, Attribute, AttributeValue, ProductAttributeValue, Card,
    WishList
)


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


@admin.action(description='check auction orders')
def check_auction_orders(modeladmin, request, queryset):
    products = AuctionProduct.objects.filter(auction=queryset[0])
    for product in products:
        if product.possible_user.wallet.balance >= product.possible_user.wallet.debt:

            product.possible_user.wallet.balance -= product.possible_user.wallet.debt
            product.possible_user.wallet.save()

            product.product.owner.wallet.balance += calculate_product_profit(product.best_price, 10)
            product.product.owner.wallet.save()

            product.product.owner = product.possible_user
            product.product.save()

            product.status = product.StatusOption.sold
            product.save()
        else:

            fine = product.best_price - product.possible_user.wallet.debt
            calculate_product_profit(fine, 10)

            product.status = product.StatusOption.not_sold
            product.save()

            product.possible_user.wallet.debt = product.best_price - fine
            product.possible_user.wallet.save()
    messages.success(request, 'all unknown products have been checked successfully')




@admin.register(AuctionProduct)
class AuctionProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'auction', 'product']


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner']


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner']


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    actions = [check_auction_orders]


admin.site.register(Category, CategoryAdmin)
