import requests

# client info
client_id = 'pW9yn0KK66EKFKTdKx93kKlFWLIANn98laV7x2yk'
client_secret = 'KO7pesMPV4884gG14Wr69aP97u01PcSyyAaQrwD506hE7MrpoeoZBBgwi7Ai5r5PsG6ij87S2xyhuY7xox34z0AoNHpGau3330UH35NgTotP6GjfeLMjUbq6fOWmFWe9'

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
