import datetime
import json
import uuid
import requests
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
#
from orders.models import Treasury
#


def send_otp(num, code):
    cri = str(uuid.uuid4())
    # new one
    payload = json.dumps({
        "receptors": [
            {
                "mobile": num,
                "clientReferenceId": cri
            }
        ],
        'templateName': 'Negar',
        "inputs": [
            {
                'param': "code",
                "value": code
            }
        ],
        'udh': True
    })
    headers = {
        'Content-Type': 'application/json',
        'ApiKey': "be8c7924979fd0faa68edd5fa269b3795017b6ab131129e58e41b940450ad5e1xixsT2zP5aRFhkEx",
    }

    res = requests.request('POST', url="https://gateway.ghasedak.me/rest/api/v1/WebService/SendOtpSMS",
                           headers=headers, data=payload)
    print(res.status_code)


def calculate_product_profit(price, percent):
    profit = (price / 100) * percent
    treasury = Treasury.objects.first()
    treasury.profit += profit
    treasury.save()
    return price - profit


def update_presenting_detail(auction_product, *args, **kwargs):
    images = auction_product.product.images.all()
    # for image in images:
    #     print(image.image.url)
    ch = get_channel_layer()
    async_to_sync(ch.group_send)
    async_to_sync(ch.group_send)('product_detail', {'type': 'update',
                                                    'product': auction_product.product,
                                                    'auction_product': auction_product,
                                                    'images': images})
