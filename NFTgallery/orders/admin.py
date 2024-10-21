from django.contrib import admin
#
from .models import (
    Treasury, Purchase
)
#

#
admin.site.register(Treasury)
#


@admin.register(Purchase)
class PurchasesAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'product', 'is_sent']
    list_filter = ['is_sent']
