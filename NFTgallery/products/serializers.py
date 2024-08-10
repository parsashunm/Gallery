from rest_framework import serializers
from .models import Product, ProductsImage


class ProductsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsImage
        exclude = ('id',)


class ProductsSerializer(serializers.ModelSerializer):
    image = ProductsImageSerializer()

    class Meta:
        model = Product
        exclude = ['slug', 'created_at']


class ProductsCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ['slug', 'created_at']
