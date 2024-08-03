from rest_framework import serializers
from .models import Product, ProductsImage


class ProductsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsImage
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    image = ProductsImageSerializer(many=True)

    class Meta:
        model = Product
        exclude = ['slug', 'created_at']
