from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
#
from .models import Auction, AuctionProduct, Product
from .tasks import stop_auction
#


@receiver(pre_save, sender=Auction)
def block_multi_auction(sender, **kwargs):
    auction = kwargs['instance']
    all_auctions = Auction.objects.filter(status=True)
    if all_auctions.exists():
        print('working \n' * 10)
        print(all_auctions.first().pk)
        print(auction.pk)
        if not auction.pk == all_auctions.first().pk:
            raise ValidationError('only one auction can be active')


# @receiver(post_save, sender=Auction)
# def stop_auction_status(sender, **kwargs):
#     auction = kwargs['instance']
#     if auction.status == True:
#         stop_auction.apply_async(args=[auction.id], countdown=10)


@receiver(post_save, sender=AuctionProduct)
def refresh_auction_product_price(sender, **kwargs):
    ap = kwargs['instance']
    ch = get_channel_layer()
    async_to_sync(ch.group_send)(f'product_{ap.pk}', {'type': 'update', 'price': ap.best_price})

#
# @receiver(pre_save, sender=Product)
# def check_product_images(sender, **kwargs):
#     image_count = kwargs['instance'].images.count()
#     if image_count < 3 or image_count > 5:
#         raise ValidationError('pictures should be between 3 and 5')

