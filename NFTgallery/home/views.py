from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
#
from products.serializers import (
    ProductsImageListSerializer,
    ProductsSerializer
)
from products.models import Product
#


class ProductsListView(ListAPIView):

    """
        no need to send anything
        will return a list of products that are buyable
    """

    serializer_class = ProductsSerializer
    queryset = Product.objects.filter(is_buyable=True)
