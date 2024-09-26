from django.db import models
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

    is_buyable = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    # uncomment when deployment
    def save(self, *args, **kwargs):
        image_count = self.images.count()
        print(image_count)
        if image_count < 3 or image_count > 5:
            raise ValidationError('pictures should be between 3 and 5')
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title


class Auction(models.Model):
    title = models.CharField(max_length=128)
    start_time = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class AuctionProduct(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='products')
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='auction')
    descriptions = models.TextField(null=True, blank=True)

    base_price = models.PositiveIntegerField()
    minimum_bid_increment = models.PositiveIntegerField()
    best_price = models.PositiveIntegerField(default=0)

    possible_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    is_presenting = models.BooleanField(default=False)

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
