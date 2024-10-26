from django.urls import path, include
#
from .views import ProductsListView
#

urlpatterns = [
    path('home/', ProductsListView.as_view(), name='products_list'),
]
