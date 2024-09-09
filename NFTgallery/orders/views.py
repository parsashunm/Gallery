from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from rest_framework.views import APIView
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
#
from accounts.models import User
from orders.models import Treasury
from orders.payment_portal import go_to_gateway_view
#


class BuyProductView(APIView):

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
