from rest_framework import serializers
#
from .models import (Product, ProductsImage, Auction, AuctionProduct)
#


class ProductsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsImage
        exclude = ('id',)


class ProductsSerializer(serializers.ModelSerializer):
    images = ProductsImageSerializer()

    class Meta:
        model = Product
        exclude = ['slug', 'created_at', 'is_buyable']


class ProductsCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ['slug', 'created_at']


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
