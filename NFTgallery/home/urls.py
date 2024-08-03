from django.urls import path, include
#
from .views import ProductsListView

app_name = 'home'

urlpatterns = [
    path('', ProductsListView.as_view(), name='products_list')
]
