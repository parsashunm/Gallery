import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from products.models import AuctionProduct


class PriceConsumer(WebsocketConsumer):

    def connect(self):
        self.product_id = self.scope['url_route']['kwargs']['product_id']
        async_to_sync(self.channel_layer.group_add)(f'product_{self.product_id}', self.channel_name)
        self.accept()
        # current_value = AuctionProduct.objects.get(pk=self.product_id).best_price
        # self.send(text_data=json.dumps({
        #     'price': current_value
        # }))

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        pass

    def update(self, data):
        updated_price = data['price']
        self.send(text_data=json.dumps({
            'price': updated_price
        }))


class AuctionProductDetailConsumer(WebsocketConsumer):

    def connect(self):
        async_to_sync(self.channel_layer.group_add)('product_detail', self.channel_name)
        self.accept()
        self.send('hi')

    def receive(self, text_data=None, bytes_data=None):
        pass

    def update(self, data):
        product = data['product']
        self.send(text_data=json.dumps({
            'title': product.title,
            'images': product.images,
            'descriptions': product.descriptions,
            'price': product.price,
        }))

    def disconnect(self, code):
        pass
