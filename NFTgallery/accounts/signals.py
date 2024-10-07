from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from products.models import Card, WishList
#
from .models import (
    User, Role, Wallet
)
#


@receiver(post_save, sender=User)
def set_default_role(sender, **kwargs):
    if kwargs['created'] and not kwargs['instance'].role:
        kwargs['instance'].role = Role.objects.get(title='buyer')
        kwargs['instance'].save()


@receiver(post_save, sender=User)
def create_user(**kwargs):
    if not hasattr(kwargs['instance'], 'wallet'):
        Wallet.objects.create(owner=kwargs['instance'])
    if not hasattr(kwargs['instance'], 'card'):
        Card.objects.create(owner=kwargs['instance'])
    if not hasattr(kwargs['instance'], 'wishlist'):
        WishList.objects.create(owner=kwargs['instance'])
