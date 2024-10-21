from django.db import models
from django.db.models import Sum
from django.utils.text import slugify
from unidecode import unidecode
from treebeard.mp_tree import MP_Node
from django.core.exceptions import ValidationError
#
from accounts.models import User
#


class ProductsImage(models.Model):
    image = models.ImageField(upload_to='products/images/%Y/%m/%d/')


class Product(models.Model):
    title = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    images = models.ManyToManyField(ProductsImage, related_name='product', blank=True)
    price = models.PositiveIntegerField()
    descriptions = models.TextField()

    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products', null=True, blank=True)

    is_buyable = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Auction(models.Model):
    title = models.CharField(max_length=128)
    start_time = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class AuctionProduct(models.Model):

    class StatusOption(models.TextChoices):
        sold = 'sold'
        unknown = 'unknown'
        not_sold = 'not sold'

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='products')
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='auction')
    descriptions = models.TextField(null=True, blank=True)

    base_price = models.PositiveIntegerField()
    minimum_bid_increment = models.PositiveIntegerField()
    best_price = models.PositiveIntegerField(default=0)

    possible_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    is_presenting = models.BooleanField(default=False)
    status = models.CharField(choices=StatusOption.choices, default=StatusOption.not_sold, max_length=64)

    def __str__(self):
        return f"{self.auction.title} - {self.product.title}"


class Category(MP_Node):
    title = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=2048, null=True, blank=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class AttributeValue(models.Model):
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=128)

    def __str__(self):
        return self.value


class Attribute(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes', null=True, blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.ManyToManyField(AttributeValue)


class Cart(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    product = models.ManyToManyField(Product, blank=True)

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def total_price(self):
        return sum(product.price for product in self.product.all())


class WishList(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ManyToManyField(Product)


class ProductTag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='tags', null=True, blank=True)
    title = models.CharField(max_length=64)
