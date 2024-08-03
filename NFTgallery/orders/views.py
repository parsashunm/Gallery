from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework.views import APIView
#
from products.models import Product
from .payment_portal import ZarinPal


class BuyProductView(APIView):

    """
    this end-point will use for purchase the arts
    """

    def get(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        request.session['order_pay'] = {'product_id': product_id}
        payment_payload = {
            'Description': 'test',
            'Phone': '12345678900',
            'Amount': product.price,
            'CallbackURL': 'http://127.0.0.1:8000/orders/purchase/verify/'
        }
        payment = ZarinPal(payment_payload)
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
        product_id = int(request.session['order_pay']['product_id'])
        product = Product.objects.get(id=product_id)
        authority = request.GET.get('Authority')
        verify_payload = {
            'Amount': product.price,
            'Authority': authority
        }
        verify = ZarinPal(verify_payload)
        result = verify.getResponse('verify')
        if result['status']:
            RefID = result['RefID']
            return HttpResponse(f"Transaction success.\nRefID: {RefID}")
        else:
            code = result['code']
            return HttpResponse(f"Transaction failed or canceled.\ncode: {code}")
