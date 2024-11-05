from rest_framework import serializers
#
from products.serializers import ProductsSerializer
#


class HomeSerializers(serializers.Serializer):
    selected_products = ProductsSerializer(many=True)
    recent_products = ProductsSerializer(many=True)
