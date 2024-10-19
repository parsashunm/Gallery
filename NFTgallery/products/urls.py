from django.urls import path
#
from .views import (CreateProductView, CreateAuctionView, CreateAuctionProductView,
                    AuctionProductDetailView, SetProductForPresentView, CloseAuctionProduct, AddToCart, CartDetailView,
                    WishListDetailView, RemoveFromWishList, RemoveFromCart, AddToWishList, CompareImagesView,
                    )
#

urlpatterns = [
    path('create/', CreateProductView.as_view(), name='create_product'),
    # path('cart/detail/<int:user_id>/', CartDetailView.as_view(), name='cart-detail'),
    # path('cart/add/<int:product_id>/', AddToCart.as_view(), name='cart-add'),
    # path('cart/remove/<int:user_id>/<int:product_id>/', RemoveFromCart.as_view(), name='remove-cart'),
    # path('wishlist/detail/<int:user_id>/', WishListDetailView.as_view(), name='wishlist-detail'),
    # path('wishlist/add/<int:product_id>/', AddToWishList.as_view(), name='wishlist-add'),
    # path('wishlist/remove/<int:user_id>/<int:product_id>/', RemoveFromWishList.as_view(), name='wishlist-remove'),
    # path('auction/create/', CreateAuctionView.as_view(), name='create-auction'),
    # path('auction/product/add/', CreateAuctionProductView.as_view(), name='add-auction-product'),
    # path('auction/product/set/<int:ap_id>/', SetProductForPresentView.as_view(), name='set-product-for_presenting'),
    # path('auction/product/close/', CloseAuctionProduct.as_view(), name='close_action_product'),
    # path('auction/product/detail/<int:auction_product_id>/',
    #      AuctionProductDetailView.as_view(), name='auction_product_detail'),
    # path('picture/compare/', CompareImagesView.as_view(), name='compare-picture'),
]
