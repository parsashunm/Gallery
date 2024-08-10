from django.urls import path, include
#
from .views import CreateProductView

app_name = 'products'

urlpatterns = [
    path('create/', CreateProductView.as_view(), name='create_product'),
]
