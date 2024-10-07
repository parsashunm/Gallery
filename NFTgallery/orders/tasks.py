# from celery import shared_task
# #
# from products.models import AuctionProduct
# from utils import calculate_product_profit
# #
#
#
# @shared_task
# def check_auction_orders():
#     products = AuctionProduct.objects.filter(status=AuctionProduct.StatusOption.unknown)
#     for product in products:
#         if product.possible_user.wallet.balance >= product.possible_user.wallet.debt:
#
#             product.possible_user.wallet.balance -= product.possible_user.wallet.debt
#             product.possible_user.wallet.save()
#
#             product.product.owner.wallet.balance += calculate_product_profit(product.best_price, 10)
#             product.product.owner.wallet.save()
#
#             product.product.owner = product.possible_user
#             product.product.save()
#
#             product.status = product.StatusOption.sold
#             product.save()
#         else:
#
#             fine = product.best_price - product.possible_user.wallet.debt
#             calculate_product_profit(fine, 10)
#
#             product.status = product.StatusOption.not_sold
#             product.save()
#
#             product.possible_user.wallet.debt = product.best_price - fine
#             product.possible_user.wallet.save()
