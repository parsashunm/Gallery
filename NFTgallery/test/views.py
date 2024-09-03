from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.views import APIView

from accounts.models import User
from .shaparak import Shaparak


class BuyProductView(APIView):

    """
    this end-point will use for purchase the arts
    needs user id and price
    """

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=int(kwargs['user_id']))
        request.session['order_pay'] = {'user_id': user.id, 'price': kwargs['price']}
        payment_payload = {
            'Description': 'test',
            'Phone': '12345678900',
            'Amount': kwargs['price'],
            'CallbackURL': 'http://127.0.0.1:8000/orders/purchase/verify/'
        }
        payment = Shaparak(payment_payload)
        result = payment.getResponse('payment')
        if result['status']:
            authority = result['authority']
            return redirect(result['STARTPAY'].format(authority))
        else:
            code = result['code']
            return HttpResponse(f"Error code: {code}")


class VerifyPurchaseView(APIView):

    """
    this view is gonna verify or reject the purchase
    """

    def get(self, request):
        user = User.objects.get(request.session['order_pay']['user_id'])
        price = int(request.session['order_pay']['price'])
        authority = request.GET.get('Authority')
        verify_payload = {
            'Amount': price,
            'Authority': authority
        }
        verify = Shaparak(verify_payload)
        result = verify.getResponse('verify')
        if result['status']:
            RefID = result['RefID']
            user.wallet.balance += price
            return HttpResponse(f"Transaction success.\nRefID: {RefID}")
        else:
            code = result['code']
            return HttpResponse(f"Transaction failed or canceled.\ncode: {code}")