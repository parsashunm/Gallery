import requests

# client info
client_id = 'SyhcphrV9q0L8vej5pOsM8xAZfbbDU2v6l2b7oUT'
client_secret = 'rMIderfSm7sxdNmJLCBTxsLZ0DpKPu4RcstYHtkhAf3hXKvxgFHVqQRO4irFz8t7KbbJ2z6iUspUjw8JimtpQgRO6gOdFYbyC2x8yINdrDQYxLkCqzWhgDFRc0mYeo1f'

# sv address
token_url = 'http://127.0.0.1:8000/ogtyfuhnjkvgmjnkbhjvghfdxcfgvbhbhjvghcfgvhhjbjknhjvghcvgbhj/token/'


def get_token(username, password):

    data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        token = response.json()
        access_token = token['access_token']
        return {'access token': access_token}
    else:
        return response.json()


def logout_user(token):
    revoke_url = 'http://localhost:8000/o/revoke_token/'

    data = {
        'token': token,
        'client_id': client_id,
        'client_secret': client_secret,
    }

    response = requests.post(revoke_url, data=data)

    if response.status_code == 200:
        return 'User logged out successfully.'
    else:
        return 'Error logging out:', response.json()
