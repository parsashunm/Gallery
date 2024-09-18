from azbankgateways.urls import az_bank_gateways_urls
from django.urls import path
#
from .views import BuyProductView, VerifyPurchaseView, ChargeWalletView

app_name = 'orders'

urlpatterns = [
    path('product/buy/<int:product_id>/', BuyProductView.as_view(), name='buy_product'),
    # path('purchase/<int:user_id>/<int:price>/', ChargeWalletView.as_view(), name='purchase_product'),
    # path('purchase/verify/', VerifyPurchaseView.as_view(), name='verify_purchase'),
    # az_bank_gateways
    # path("bankgateways/", az_bank_gateways_urls(), name='purchase_product'),
    # path("test/", az_bank_gateways_urls(), name='verify_purchase'),

]
