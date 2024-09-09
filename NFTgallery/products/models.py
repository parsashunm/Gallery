from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from treebeard.mp_tree import MP_Node
#
from accounts.models import User
#


class Product(models.Model):
    title = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    images = models.ManyToManyField('ProductsImage', related_name='product', blank=True)
    price = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, null=True, blank=True)
    descriptions = models.TextField()

    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products', null=True, blank=True)

    is_buyable = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def get_slug(self):
        try:
            self.slug = slugify(self.title[:30])
        except:
            self.slug = slugify(unidecode(self.title[:30]))
        print(self.slug)


class ProductsImage(models.Model):
    image = models.ImageField(upload_to='product/%Y/%m/%d/')


class Auction(models.Model):
    title = models.CharField(max_length=128)
    start_time = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class AuctionProduct(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='products')
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='auction')
    base_price = models.PositiveIntegerField()
    minimum_bid_increment = models.PositiveIntegerField()
    best_price = models.PositiveIntegerField(default=0)
    possible_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Category(MP_Node):
    title = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=2048, null=True, blank=True)
    is_public = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
