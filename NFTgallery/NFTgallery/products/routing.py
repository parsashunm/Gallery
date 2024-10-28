from django.urls import path
from .consumers import PriceConsumer, AuctionProductDetailConsumer

websocket_urlpatterns = [
    path('auction/product/price/<int:product_id>/', PriceConsumer.as_asgi(), name='update_auction_product_price'),
    path('auction/product/detail/', AuctionProductDetailConsumer.as_asgi(), name='update_auction_product'),
]