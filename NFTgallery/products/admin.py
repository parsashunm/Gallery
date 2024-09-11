from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

#
from .models import (
    Product, ProductsImage, Auction, AuctionProduct, Category, ProductAttributeValue, ProductClass, ProductAttribute,
    OptionGroup, OptionGroupValue, Option
)
#
admin.site.register(Auction)
admin.site.register(ProductAttribute)
admin.site.register(OptionGroup)
admin.site.register(OptionGroupValue)
admin.site.register(Option)
#


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 0


class ProductAttributeInline(admin.StackedInline):
    model = ProductAttribute
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', 'price']
    inlines = [ProductAttributeValueInline]


@admin.register(ProductClass)
class ProductClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'attribute_count')
    inlines = [ProductAttributeInline]
    prepopulated_fields = {"slug": ("title",)}

    def attribute_count(self, obj):
        return obj.attributes.count()


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


class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)


admin.site.register(Category, CategoryAdmin)
