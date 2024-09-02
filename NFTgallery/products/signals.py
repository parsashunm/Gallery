from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
#
from .models import Auction, AuctionProduct
from .tasks import stop_auction
#


@receiver(pre_save, sender=Auction)
def block_multi_auction(sender, **kwargs):
    auction = kwargs['instance']
    if Auction.objects.exists() and not auction.pk:
        raise ValidationError('only one auction can be exist')


@receiver(post_save, sender=Auction)
def stop_auction_status(sender, **kwargs):
    auction = kwargs['instance']
    if auction.status == True:
        stop_auction.apply_async(args=[auction.id], countdown=10)


@receiver(post_save, sender=AuctionProduct)
def refresh_auction_product_price(sender, **kwargs):
    ap = kwargs['instance']
    ch = get_channel_layer()
    async_to_sync(ch.group_send)(f'product_{ap.pk}', {'type': 'update', 'price': ap.best_price})

