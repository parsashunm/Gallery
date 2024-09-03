import datetime
import json
import uuid
import requests


def send_otp(num, code):
    cri = str(uuid.uuid4())
    # new one
    payload = json.dumps({
        "receptors": [
            {
                "mobile": num,
                "clientReferenceId": cri
            }
        ],
        'templateName': 'Negar',
        "inputs": [
            {
                'param': "code",
                "value": code
            }
        ],
        'udh': True
    })
    headers = {
        'Content-Type': 'application/json',
        'ApiKey': "be8c7924979fd0faa68edd5fa269b3795017b6ab131129e58e41b940450ad5e1xixsT2zP5aRFhkEx",
    }

    res = requests.request('POST', url="https://gateway.ghasedak.me/rest/api/v1/WebService/SendOtpSMS",
                           headers=headers, data=payload)
