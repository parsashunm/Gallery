from django.db import models
from django.core.exceptions import ValidationError

from accounts.models import User, Address
from products.models import Product


class Treasury(models.Model):
    title = models.CharField(max_length=32)
    users_balance = models.PositiveIntegerField(default=0)
    profit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Purchase(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='purchases', null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    bought_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.buyer.username} - {self.product.title}"
