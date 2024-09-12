from django.core.management.base import BaseCommand, CommandError
from orders.models import Treasury
from accounts.models import Role


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            Role.objects.create(title='buyer')
            Role.objects.create(title='artist')
            Role.objects.create(title='presenter')
            self.stdout.write('roles created')
        except:
            raise CommandError('roles already created')
        try:
            Treasury.objects.create(title='main treasury')
            self.stdout.write('main treasury created')
        except:
            raise CommandError('treasury already crated')
