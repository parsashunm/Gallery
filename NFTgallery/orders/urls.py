from django.urls import path
#
from .views import BuyProductView, VerifyPurchaseView

app_name = 'orders'

urlpatterns = [
    # path('purchase/<int:product_id>/', BuyProductView.as_view(), name='purchase_product'),
    path('purchase/<int:user_id>/<int:price>/', BuyProductView.as_view(), name='purchase_product'),
    path('purchase/verify/', VerifyPurchaseView.as_view(), name='verify_purchase'),
]