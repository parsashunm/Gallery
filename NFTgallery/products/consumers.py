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
        self.send('connected')

    def receive(self, text_data=None, bytes_data=None):
        pass

    def update(self, data):
        auction_product = data['auction_product']
        product = data['product']
        images = data['images']
        images_url = [image.image.url for image in images]
        self.send(text_data=json.dumps({
            'title': product.title,
            'images': images_url,
            'descriptions': auction_product.descriptions,
            'base_price': auction_product.base_price,
            'best_price': auction_product.best_price,
        }))

    def disconnect(self, code):
        pass
