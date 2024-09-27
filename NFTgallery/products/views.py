from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from orders.models import Treasury
from permissions import IsSpecificUser, IsPresenter, IsArtist
from utils import calculate_product_profit, update_presenting_detail
#
from .serializers import (CreateAuctionProductSerializer, ProductsCreateSerializer, CreateAuctionSerializer,
                          ActionProductSerializer, ProductsSerializer)
from .models import (Product, Auction, AuctionProduct)
#


class CreateProductView(CreateAPIView):

    """
    creat a Product
    \nsend image id for image field
    \nowner will be a user id
    \ncategory have not be a parent like paint but miniature or classic is ok for e.g
    \n.
    \n.
    \n.
    \nabout attributes field:
    \nattribute value is an object of Attributes
    \nbut you have to send one of them / for e.g:
    \n you set color for attribute / now you must set one or many value for it such as green, white, red ...
    """

    serializer_class = ProductsCreateSerializer
    queryset = Product.objects.all()
    permission_classes = [IsArtist]


class CreateAuctionView(CreateAPIView):

    """
    just need a title
    \n status will set to False by default
    """

    serializer_class = CreateAuctionSerializer
    queryset = Auction.objects.all()


class CreateAuctionProductView(APIView):

    """
    needs 'product id' for product field
    """

    serializer_class = CreateAuctionProductSerializer
    queryset = Auction.objects.all()

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data)
        return Response(ser_data.errors)


class AuctionProductDetailView(APIView):

    serializer_class = ActionProductSerializer
    queryset = AuctionProduct.objects.all()

    def get(self, request, auction_product_id):
        auction_product = self.queryset.get(pk=auction_product_id)
        ser_data = self.serializer_class(auction_product)
        return Response(ser_data.data)


class SetProductForPresentView(APIView):
  
    permission_classes = [IsPresenter]

    def post(self, request):
        auction_product = AuctionProduct.objects.get(pk=request.data['id'])
        auction_product.is_presenting = True
        update_presenting_detail(AuctionProduct)
        return Response('done')


# class ClosePresentAuctionProduct(APIView):
#
#     permission_classes = [IsPresenter]
#
#     def post(self, request):
#         auction_product = AuctionProduct.objects.get(pk=request.data['id'])
#         auction_product.is_presenting = False
