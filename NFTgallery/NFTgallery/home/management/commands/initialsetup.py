import time
from django.core.management.base import BaseCommand, CommandError
from oauth2_provider.models import Application
#
from orders.models import Treasury
from accounts.models import Role
#


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            self.stdout.write('creating roles . . .')
            Role.objects.create(title='buyer')
            Role.objects.create(title='artist')
            Role.objects.create(title='presenter')
            self.stdout.write('roles created')
        except:
            self.stdout.write('roles already created')
        try:
            self.stdout.write('creating treasury . . .')
            Treasury.objects.create(title='main treasury')
            self.stdout.write('main treasury created')
        except:
            self.stdout.write('treasury already crated')
        try:
            self.stdout.write('creating a login app')
            Application.objects.create(
                name='main',
                client_type=Application.CLIENT_CONFIDENTIAL,
                authorization_grant_type=Application.GRANT_PASSWORD,
                client_id='QO12SCTCVYwMhzLDjAhb6d1jsXRsgQyQr13Rkhr3',
                client_secret='1ftLrUNmBIKaX5nwt2KLUsdMJdkvhp5gg7TpCAorNvlMdDpXRBt8qBDC6utTbN6mlR2DPvCzaLKto2BjHjdMSyEgJUumvCxEeARXqBaYd3D9Nf7LisBq4Z8udbHroMIU',
            )
            self.stdout.write('login app successfully created')
        except:
            self.stdout.write('we already have one login app')
        self.stdout.write('setup successful now you can run server')
        self.stdout.write('wish luck :)')
