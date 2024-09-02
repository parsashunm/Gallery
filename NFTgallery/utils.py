import json
import requests


def send_otp(num, code):
    # instance
    # sms_api = ghasedak_sms.Ghasedak(api_key="be8c7924979fd0faa68edd5fa269b3795017b6ab131129e58e41b940450ad5e1xixsT2zP5aRFhkEx")
    # res = sms_api.send_otp_sms(num, code)

    # new one
    payload = json.dumps({
        "receptors": [
            {
                "mobile": num,
                "clientReferenceId": "8"
            }
        ],
        'templateName': 'Ghasedak',
        "inputs": [
            {
                'param': "code",
                "value": code
            }
        ],
    })
    headers = {
        'Content-Type': 'application/json',
        'ApiKey': "be8c7924979fd0faa68edd5fa269b3795017b6ab131129e58e41b940450ad5e1xixsT2zP5aRFhkEx",
    }

    requests.request('POST', url="https://gateway.ghasedak.me/rest/api/v1/WebService/SendOtpSMS",
                     headers=headers, data=payload)
