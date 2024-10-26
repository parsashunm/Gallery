from celery import shared_task
#
from products.models import AuctionProduct
from utils import calculate_product_profit
#
