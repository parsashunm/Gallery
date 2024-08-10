from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
#
from .serializers import ProductsSerializer, ProductsCreateSerializer
from NFT_SetUp.NFT_Utils import create_nft
from .models import Product
#


class CreateProductView(CreateAPIView):

    """
    creat a Product
    \nsend image id for image field
    """

    serializer_class = ProductsCreateSerializer
    queryset = Product.objects.all()
