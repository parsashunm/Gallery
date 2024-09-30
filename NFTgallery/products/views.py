from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
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
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors)


class AuctionProductDetailView(APIView):

    serializer_class = ActionProductSerializer
    queryset = AuctionProduct.objects.all()

    def get(self, request, auction_product_id):
        auction_product = self.queryset.get(pk=auction_product_id)
        ser_data = self.serializer_class(auction_product)
        return Response(ser_data.data)


class SetProductForPresentView(APIView):

    """
    needs auction product id in url
    """

    permission_classes = [IsPresenter]

    def get(self, request, ap_id):
        if AuctionProduct.objects.filter(is_presenting=True).exists():
            return Response('close all the products that are presenting first', status=status.HTTP_400_BAD_REQUEST)
        auction_product = AuctionProduct.objects.get(id=ap_id)
        auction_product.is_presenting = True
        auction_product.save()
        update_presenting_detail(auction_product)
        return Response('done')


class CloseAuctionProduct(APIView):

    permission_classes = [IsPresenter]
    queryset = AuctionProduct.objects.all()

    def post(self, request):
        auction_product = get_object_or_404(AuctionProduct, is_presenting=True)
        if auction_product.possible_user:
            if auction_product.possible_user.wallet.debt == 0:
                auction_product.possible_user.wallet.blocked_balance -= auction_product.best_price
                auction_product.product.owner = auction_product.possible_user
                auction_product.status = auction_product.StatusOption.sold
                auction_product.save()
                auction_product.product.save()
                auction_product.possible_user.wallet.save()
                update_presenting_detail(auction_product=auction_product, empty=True)
                return Response('done', status=status.HTTP_200_OK)
            auction_product.status = auction_product.StatusOption.unknown
            return Response('mojudi shoma kafi nemibashad lotfa hesab khod ra ta sa`at 00:00 sharj konid')
        return Response('kharidari baraye in mahsol peyda nashod')
