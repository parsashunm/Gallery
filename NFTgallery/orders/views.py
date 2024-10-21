from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from azbankgateways import (
    models as bank_models,
    default_settings as settings,
)
#
from accounts.models import User
from orders.models import Treasury, Purchase
from orders.payment_portal import go_to_gateway_view
from products.models import Product, AuctionProduct, ProductsImage
from utils import calculate_product_profit, update_presenting_detail


#


class ChargeWalletView(APIView):

    """
    this end-point will use for purchase the arts
    needs user id and price
    """

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=int(kwargs['user_id']))
        request.session['order_pay'] = {'user_id': user.id, 'price': kwargs['price']}
        go_to_gateway_view(request, kwargs['price'], user.phone)


class VerifyPurchaseView(APIView):

    """
    this view is gonna verify or reject the purchase
    """

    def get(self, request):
        user = User.objects.get(id=int(request.session['order_pay']['user_id']))
        tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
        if not tracking_code:
            raise Http404

        try:
            bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
        except bank_models.Bank.DoesNotExist:
            raise Http404

        if bank_record.is_success:
            balance = int(request.session['order_pay']['price'])
            user.wallet.balance += balance
            Treasury.objects.first().users_balance += balance
            return HttpResponse("پرداخت با موفقیت انجام شد.")

        return HttpResponse(
            "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت."
        )


class BuyProductView(APIView):
    """
        we just need product id in url
    """

    permission_classes = [IsAuthenticated]
    serializer_class = None

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['product_id'])
        user = request.user
        if user.wallet.balance >= product.price and user.wallet.debt < 1:
            print(user.wallet.balance)
            print(product.price)
            user.wallet.balance -= product.price
            user.wallet.save()
            product.owner.wallet.balance += calculate_product_profit(product.price, 10)
            product.owner.wallet.save()
            product.is_buyable = False
            product.owner = user
            product.save()
            return Response('you bought the product successfully')
        return Response("your balance isn't enough")


class OfferRegisterView(APIView):

    """
        needs just id as auction product id and offer in request body
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        auction_product = AuctionProduct.objects.get(id=request.data['id'])
        offer = int(request.data['offer'])
        best_price = max(auction_product.best_price, auction_product.base_price)
        if auction_product.is_presenting:
            if (request.user.wallet.balance * 2) >= offer:
                if offer >= (best_price + auction_product.minimum_bid_increment):
                    possible_user = request.user
                    clean_offer = offer

                    try:
                        last_offer_user = auction_product.possible_user
                        past_best_price = auction_product.best_price
                        clean_price = past_best_price
                        if last_offer_user.wallet.blocked_balance < past_best_price:
                            clean_price = past_best_price - last_offer_user.wallet.debt
                            last_offer_user.wallet.debt -= past_best_price - last_offer_user.wallet.blocked_balance
                        last_offer_user.wallet.blocked_balance -= clean_price
                        last_offer_user.wallet.balance += past_best_price
                        last_offer_user.wallet.save()
                    except:
                        pass

                    if offer > possible_user.wallet.balance:
                        possible_user.wallet.debt += offer - possible_user.wallet.balance
                        clean_offer = offer - possible_user.wallet.debt

                    possible_user.wallet.balance -= clean_offer
                    possible_user.wallet.blocked_balance += clean_offer
                    possible_user.wallet.save()

                    auction_product.best_price = offer
                    auction_product.possible_user = possible_user
                    auction_product.save()

                    update_presenting_detail(auction_product)

                    return Response('done')
                return Response("please offer higher price")
            return Response("you dont have that many")
        return Response("this product isn't presenting")


class CartPaymentView(APIView):
    """
    just need an address-id
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        if user.wallet.balance >= user.cart.total_price():
            for product in user.cart.product.all():
                if product.is_buyable:
                    user.wallet.balance -= product.price
                    product.owner.wallet.balance += calculate_product_profit(product.price, 10)
                    product.owner = user
                    product.is_buyable = False
                    user.wallet.save()
                    product.owner.wallet.save()
                    product.save()
                    Purchase.objects.create(buyer=user, product=product, address_id=data['address'])
            user.cart.product.clear()
            return Response('the cart was purchase successfully')
        return Response('you dont have enough money')

