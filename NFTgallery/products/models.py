from django.db import models
from accounts.models import User
from django.utils.text import slugify
from unidecode import unidecode


class Product(models.Model):
    title = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    image = models.ForeignKey('ProductsImage', on_delete=models.PROTECT, related_name='product')
    price = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, null=True)
    descriptions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        try:
            self.slug = slugify(self.title[:30])
        except:
            self.slug = slugify(unidecode(self.title[:30]))
        super().save(force_insert, force_update, using, update_fields)


class ProductsImage(models.Model):
    image = models.ImageField()
