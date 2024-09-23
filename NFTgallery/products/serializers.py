from rest_framework import serializers
#
from .models import (Product, ProductsImage, Auction, AuctionProduct, Category, ProductAttributeValue)
#


class ProductsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsImage
        fields = ['image']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

        extra_kwargs = {
            'path': {'write_only': True},
            'depth': {'write_only': True},
            'numchild': {'write_only': True},
            'description': {'write_only': True},
            'is_public': {'write_only': True},
        }


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        fields = ['attribute', 'value']


class ProductsSerializer(serializers.ModelSerializer):
    images = ProductsImageSerializer(many=True)
    attributes = ProductAttributeValueSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Product
        exclude = ['created_at', 'is_buyable']


class CreateProductAttributeValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttributeValue
        exclude = ['id', 'product']


class ProductsCreateSerializer(serializers.ModelSerializer):

    attributes = CreateProductAttributeValueSerializer(many=True)

    class Meta:
        model = Product
        exclude = ['id', 'created_at']

    def create(self, validated_data):

        attributes_data = validated_data.pop('attributes')
        images = validated_data.pop('images')

        product = Product.objects.create(**validated_data)
        product.images.set(images)

        for attribute_data in attributes_data:
            values = attribute_data.pop('value')
            product_attribute_value = ProductAttributeValue.objects.create(product=product, **attribute_data)

            product_attribute_value.value.set(values)

        return product


class CreateAuctionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auction
        fields = ['title']


class CreateAuctionProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuctionProduct
        fields = ['product', 'base_price', 'minimum_bid_increment']

    def create(self, validated_data):
        validated_data['auction'] = Auction.objects.first()
        return super().create(validated_data)


class AuctionProductSerializer(serializers.ModelSerializer):

    images = ProductsImageSerializer()

    class Meta:
        model = Product
        fields = ['title', 'owner', 'images', 'descriptions']


class ActionProductSerializer(serializers.ModelSerializer):

    product = AuctionProductSerializer()

    class Meta:
        model = AuctionProduct
        fields = ['product', 'base_price', 'minimum_bid_increment']
