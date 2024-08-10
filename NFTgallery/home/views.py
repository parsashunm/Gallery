from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
#
from products.serializers import (
    ProductsImageSerializer,
    ProductsSerializer,
)
from products.models import Product
#


class ProductsListView(ListAPIView):

    """
    no need to send anything
    """

    serializer_class = ProductsSerializer
    queryset = Product.objects.all()
