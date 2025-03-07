import numpy as np
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
import cv2
from skimage.metrics import structural_similarity as ssim
from django.shortcuts import get_object_or_404
#
from permissions import IsSpecificUser, IsPresenter, IsArtist
from orders.models import Purchase
from utils import calculate_product_profit, update_presenting_detail
from .serializers import (CreateAuctionProductSerializer, ProductsCreateSerializer, CreateAuctionSerializer,
                          ActionProductSerializer, ProductsSerializer, CartDetailSerializer, WishListSerializer,
                          CompareImagesSerializers)
from accounts.models import User
from .models import (Product, Auction, AuctionProduct, Cart, WishList)
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
        return Response({"detail": 'done'})


class CloseAuctionProduct(APIView):

    permission_classes = [IsPresenter]
    queryset = AuctionProduct.objects.all()

    def post(self, request):
        # auction_product = get_object_or_404(AuctionProduct, is_presenting=True)
        auction_product = AuctionProduct.objects.select_related('possible_user__wallet', 'product__owner').get(is_presenting=True)
        if auction_product.possible_user:
            if auction_product.possible_user.wallet.debt == 0:

                with transaction.atomic():
                    auction_product.possible_user.wallet.blocked_balance -= auction_product.best_price
                    auction_product.product.owner.wallet.balance += calculate_product_profit(
                        auction_product.best_price, auction_product.product.category.get_parent().income
                    )
                    auction_product.product.owner = auction_product.possible_user
                    auction_product.status = auction_product.StatusOption.sold

                    Purchase.objects.create(buyer=auction_product.possible_user,
                                            address='purchased in Auction', product=auction_product)

                    auction_product.save()
                    auction_product.product.save()
                    auction_product.possible_user.wallet.save()
                    auction_product.product.owner.wallet.save()

                update_presenting_detail(auction_product=auction_product, empty=True)
                return Response({"detail": 'done'}, status=status.HTTP_200_OK)

            auction_product.possible_user.wallet.blocked_balance -= auction_product.best_price - auction_product.possible_user.wallet.debt
            auction_product.possible_user.wallet.save()
            auction_product.status = auction_product.StatusOption.unknown

            auction_product.save()
            return Response({"detail": 'mojudi shoma kafi nemibashad lotfa hesab khod ra ta sa`at 00:00 sharj konid'})
        return Response({"detail": 'kharidari baraye in mahsol peyda nashod'})


class AddToCart(APIView):
    """
    add a product to cart
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        card = Cart.objects.get(owner=request.user)
        product = Product.objects.get(pk=product_id)
        if product.is_buyable:
            card.product.add(product)
            card.save()
            return Response({"detail": 'done'})
        return Response({"error": "product isn't buyable"})


class CartDetailView(APIView):

    """
    view cart list
    """

    permission_classes = [IsSpecificUser]

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        card = user.cart
        for product in card.product:
            if not product.is_buyable:
                card.product.remove(product)
                card.save()
        srz_data = CartDetailSerializer({
            'product': card.product.all(),
            'total': card.total_price()
        })
        return Response(srz_data.data)


class RemoveFromCart(APIView):

    """
    remove a product from cart
    """

    permission_classes = [IsSpecificUser]

    def get(self, request, user_id, product_id):
        card = User.objects.get(pk=user_id).card
        product = Product.objects.get(pk=product_id)
        card.product.remove(product)
        return Response({"detail": 'done'})


class AddToWishList(APIView):

    """
    add a product to wishlist
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        wishlist = WishList.objects.get(owner=request.user)
        product = Product.objects.get(pk=product_id)
        wishlist.product.add(product)
        wishlist.save()
        return Response({"detail": 'done'})


class WishListDetailView(RetrieveAPIView):

    """
    view wishlist items
    """

    permission_classes = [IsSpecificUser]

    serializer_class = WishListSerializer
    queryset = WishList.objects.all()
    lookup_field = 'owner'
    lookup_url_kwarg = 'user_id'


class RemoveFromWishList(APIView):

    """
    remove a product from wishlist
    """

    permission_classes = [IsSpecificUser]

    def get(self, request, user_id, product_id):
        wishlist = User.objects.get(pk=user_id).wishlist
        product = Product.objects.get(pk=product_id)
        wishlist.product.remove(product)
        return Response({"detail": 'done'})


class CompareImagesView(APIView):

    """
    it compares two images and shows how similar they are.
    """

    permission_classes = [IsArtist]

    def post(self, request):
        srz_data = CompareImagesSerializers(data=request.data)
        if srz_data.is_valid():
            image1 = srz_data.validated_data['image1']
            image2 = srz_data.validated_data['image2']

            img1 = cv2.imdecode(np.frombuffer(image1.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imdecode(np.frombuffer(image2.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

            img1 = cv2.resize(img1, (256, 256))
            img2 = cv2.resize(img2, (256, 256))

            score, _ = ssim(img1, img2, full=True)
            similarity_percentage = score * 100

            return Response({"detail": f"similarity_percentage : {similarity_percentage:.2f}%"})

        return Response(srz_data.errors, status=400)
