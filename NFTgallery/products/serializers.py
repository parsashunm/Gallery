from rest_framework import serializers
#
from .models import (Product, ProductsImage, Auction, AuctionProduct, Category, ProductClass, Option, OptionGroup,
                     ProductAttribute)
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


class OptionGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionGroup
        fields = '__all__'


class OptionSerializer(serializers.ModelSerializer):

    option_group = OptionGroupSerializer()

    class Meta:
        model = Option
        exclude = ['required']


class ProductClassSerializer(serializers.ModelSerializer):

    options = OptionSerializer(many=True)

    class Meta:
        model = ProductClass
        fields = '__all__'

        extra_kwargs = {
            'options': {'write_only': True},
            'title': {'write_only': True},
            'slug': {'write_only': True},
            'description': {'write_only': True},
        }


class ProductAttributesSerializer(serializers.ModelSerializer):

    product_class = ProductClassSerializer()
    option_group = OptionGroupSerializer()

    class Meta:
        model = ProductAttribute
        fields = '__all__'

        extra_kwargs = {
            'product_class': {'write_only': True},
            'type': {'write_only': True},
            'required': {'write_only': True},
        }


class ProductsSerializer(serializers.ModelSerializer):
    images = ProductsImageSerializer(many=True)

    category = CategorySerializer()
    product_class = ProductClassSerializer()
    attributes = ProductAttributesSerializer(many=True)

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
