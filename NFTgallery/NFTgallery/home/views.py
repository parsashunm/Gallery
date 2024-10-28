from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
#
from home.serializers import HomeSerializers
from products.models import Product
#


class ProductsListView(APIView):

    """
        no need to send anything
        will return a list of products that are buyable
    """

    serializer_class = HomeSerializers

    def get(self, request):
        q_set = Product.objects.all()
        srz_data = self.serializer_class({
            'selected_products': q_set.filter(is_buyable=True, tags__title='home'),
            'recent_products': q_set.order_by('-created_at')[:9]
        })
        return Response(srz_data.data)
