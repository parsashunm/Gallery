from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from orders.models import Treasury
from utils import calculate_product_profit
#
from .serializers import (CreateAuctionProductSerializer, ProductsCreateSerializer, CreateAuctionSerializer,
                          ActionProductSerializer, ProductsSerializer, )
from .models import (Product, Auction, AuctionProduct)
#


class CreateProductView(CreateAPIView):

    """
    creat a Product
    \nsend image id for image field
    \nowner will be a user id
    \ncategory have not be a parent like painting but miniature or classic is ok for e.g
    \n.
    \n.
    \n.
    \nabout attributes field:
    \nall fields what are in are optional except attribute
    \nattribute value is an object of Product Attributes
    \nbut you have to send one of them / for e.g:
    \n you set color attribute / now you must set one or many value for it such as green, white, red ...
    """

    serializer_class = ProductsCreateSerializer
    queryset = Product.objects.all()


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


class OfferRegisterView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        auction_product = AuctionProduct.objects.get(id=request.data['id'])
        offer = int(request.data['offer'])
        best_price = max(auction_product.best_price, auction_product.base_price)
        if (request.user.wallet.balance * 2) >= offer:
            if offer >= (best_price + auction_product.minimum_bid_increment):
                possible_user = request.user

                try:
                    lost_offer_user = auction_product.possible_user
                    past_best_price = auction_product.best_price
                    lost_offer_user.wallet.blocked_balance -= past_best_price
                    lost_offer_user.wallet.balance += past_best_price
                except:
                    pass

                possible_user.wallet.balance -= offer
                possible_user.wallet.blocked_balance += offer
                auction_product.best_price = offer
                auction_product.possible_user = possible_user
                auction_product.save()

                return Response('done')
            return Response("please offer higher price")
        return Response("you dont have that many")
