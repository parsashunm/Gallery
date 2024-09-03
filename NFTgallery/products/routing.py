from django.urls import path
from .consumers import PriceConsumer

websocket_urlpatterns = [
    path('auction/product/price/<int:product_id>/', PriceConsumer.as_asgi(), name='update_auction_product_price')
]