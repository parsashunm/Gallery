from django.urls import path
#
from .views import BuyProductView, VerifyPurchaseView, ChargeWalletView, OfferRegisterView, CartPaymentView

#

urlpatterns = [
    path('product/buy/<int:product_id>/', BuyProductView.as_view(), name='buy_product'),
    # path('auction/product/offer/', OfferRegisterView.as_view(), name='new_offer'),
    # path('purchase/<int:user_id>/<int:price>/', ChargeWalletView.as_view(), name='purchase_product'),
    # path('purchase/verify/', VerifyPurchaseView.as_view(), name='verify_purchase'),
    # az_bank_gateways
    # path("test/", az_bank_gateways_urls(), name='verify_purchase'),
    # path('cart/pay/', CartPaymentView.as_view(), name='cart-pay'),
]
