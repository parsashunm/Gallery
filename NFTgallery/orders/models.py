from django.db import models
#
from accounts.models import User
from products.models import Product
#


class Auction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions')
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    bace_price = models.PositiveIntegerField()
    minimum_bid_increment = models.PositiveIntegerField()
    auction_time = models.DateTimeField()
