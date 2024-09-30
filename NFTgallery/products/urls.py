from django.urls import path
#
from .views import (CreateProductView, CreateAuctionView, CreateAuctionProductView,
                    AuctionProductDetailView, SetProductForPresentView, CloseAuctionProduct)
#

app_name = 'products'

urlpatterns = [
    path('create/', CreateProductView.as_view(), name='create_product'),
    # path('auction/create/', CreateAuctionView.as_view(), name='create_auction'),
    # path('auction/product/add/', CreateAuctionProductView.as_view(), name='add_auction_product'),
    # path('auction/product/set/<int:ap_id>/', SetProductForPresentView.as_view(), name='set_product_for_presenting'),
    # path('auction/product/close/', CloseAuctionProduct.as_view(), name='close_action_product'),
    # path('auction/product/detail/<int:auction_product_id>/', AuctionProductDetailView.as_view(), name='auction_product_detail'),
]
