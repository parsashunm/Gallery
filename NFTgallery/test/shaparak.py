import requests
import json
from django.conf import settings
from django.shortcuts import redirect

sandbox = 'sandbox' if settings.SANDBOX else 'www'
ZP_API_REQUEST = f"https://sep.shaparak.ir/payment.aspx/"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


class Shaparak:
    def __init__(self, data=dict):

        self.request_data = data
        self.request_data["MerchantID"] = settings.MERCHANT
        self.request_header = {
            'content-type': 'application/json',
            'content-length': str(len(self.request_data))
        }

    def getResponse(self, flag):
        url = ZP_API_REQUEST if flag == 'payment' else ZP_API_VERIFY
        try:
            response = requests.post(
                url=url,
                data=json.dumps(self.request_data),
                headers=self.request_header,
                timeout=30
            ).json()
            if response['Status'] == 100:
                if flag == 'payment':
                    authority = response['Authority']
                    return {'status': True, 'STARTPAY': ZP_API_STARTPAY + str(authority), 'authority': authority}
                else:
                    return {'status': True, 'RefID': response['RefID']}

            return {'status': False, 'code': str(response['Status'])}

        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}
