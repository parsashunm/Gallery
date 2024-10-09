from django.urls import path
#
from .views import (CreateProductView, CreateAuctionView, CreateAuctionProductView,
                    AuctionProductDetailView, SetProductForPresentView, CloseAuctionProduct, AddToCard, CardDetailView,
                    WishListDetailView, RemoveFromWishList, RemoveFromCard, AddToWishList,
                    )
#

urlpatterns = [
    path('create/', CreateProductView.as_view(), name='create_product'),
    # path('card/detail/<int:user_id>/', CardDetailView.as_view(), name='card-detail'),
    # path('card/add/<int:product_id>/', AddToCard.as_view(), name='card-add'),
    # path('card/remove/<int:user_id>/<int:product_id>/', RemoveFromCard.as_view(), name='remove-card'),
    # path('wishlist/detail/<int:user_id>/', WishListDetailView.as_view(), name='wishlist-detail'),
    # path('wishlist/add/<int:product_id>/', AddToWishList.as_view(), name='wishlist-add'),
    # path('wishlist/remove/<int:user_id>/<int:product_id>/', RemoveFromWishList.as_view(), name='wishlist-remove'),
    # path('auction/create/', CreateAuctionView.as_view(), name='create-auction'),
    # path('auction/product/add/', CreateAuctionProductView.as_view(), name='add-auction-product'),
    # path('auction/product/set/<int:ap_id>/', SetProductForPresentView.as_view(), name='set-product-for_presenting'),
    # path('auction/product/close/', CloseAuctionProduct.as_view(), name='close_action_product'),
    # path('auction/product/detail/<int:auction_product_id>/',
    #      AuctionProductDetailView.as_view(), name='auction_product_detail'),
]
