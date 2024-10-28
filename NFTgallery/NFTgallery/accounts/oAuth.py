import requests
from django.shortcuts import redirect
from rest_framework.reverse import reverse_lazy

# client info
client_id = 'QO12SCTCVYwMhzLDjAhb6d1jsXRsgQyQr13Rkhr3'
client_secret = '1ftLrUNmBIKaX5nwt2KLUsdMJdkvhp5gg7TpCAorNvlMdDpXRBt8qBDC6utTbN6mlR2DPvCzaLKto2BjHjdMSyEgJUumvCxEeARXqBaYd3D9Nf7LisBq4Z8udbHroMIU'

# sv address
token_url = reverse_lazy('create_token')
revoke_url = reverse_lazy('revoke_token')


def get_token(request, username, password):

    data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(request.build_absolute_uri(token_url), data=data)

    if response.status_code == 200:
        token = response.json()
        access_token = token['access_token']
        return {'access token': access_token}
    else:
        return response.json()


def logout_user(request, token):

    data = {
        'token': token,
        'client_id': client_id,
        'client_secret': client_secret,
    }

    response = requests.post(request.build_absolute_uri(revoke_url), data=data)

    if response.status_code == 200:
        return 'User logged out successfully.'
    else:
        return 'Error logging out:', response.json()
