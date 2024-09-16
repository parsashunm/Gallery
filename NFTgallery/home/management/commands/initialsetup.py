import time
from django.core.management.base import BaseCommand, CommandError
from orders.models import Treasury
from accounts.models import Role


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            self.stdout.write('creating roles . . .')
            Role.objects.create(title='buyer')
            Role.objects.create(title='artist')
            Role.objects.create(title='presenter')
            time.sleep(3)
            self.stdout.write('roles created')
        except:
            raise CommandError('roles already created')
        try:
            self.stdout.write('creating treasury . . .')
            Treasury.objects.create(title='main treasury')
            time.sleep(3)
            self.stdout.write('main treasury created')
        except:
            raise CommandError('treasury already crated')
        self.stdout.write('setup successful now you can run server')
        self.stdout.write('wish luck :)')
