from celery import shared_task
#
from .models import Auction
#

@shared_task
def stop_auction(auction_id):
    auction = Auction.objects.get(pk=auction_id)
    auction.status = False
    auction.save()
