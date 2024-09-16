from django.urls import path
#
from .views import (CreateProductView, CreateAuctionView, CreateAuctionProductView,
                    AuctionProductDetailView, OfferRegisterView, BuyProductView)
#

app_name = 'products'

urlpatterns = [
    path('create/', CreateProductView.as_view(), name='create_product'),
    path('buy/<int:product_id>/', BuyProductView.as_view(), name='buy_product'),
    # path('auction/create/', CreateAuctionView.as_view(), name='create_auction'),
    # path('auction/product/add/', CreateAuctionProductView.as_view(), name='add_auction_product'),
    # path('auction/product/detail/<int:auction_product_id>/', AuctionProductDetailView.as_view(), name='auction_product_detail'),
    # path('auction/product/offer/', OfferRegisterView.as_view(), name='new_offer')
]
