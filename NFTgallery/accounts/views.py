# from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView, Response
from rest_framework.generics import CreateAPIView
from django.contrib.auth import authenticate
#
from .serializers import CreateAccountSerializer
from .models import User
from oAuth import get_token, logout_user
#


class UserCreateView(CreateAPIView):
    """
    needs:
    \n- username/phone/password/pass2(confirm password)
    """
    serializer_class = CreateAccountSerializer
    queryset = User.objects.all()


class UserLoginView(APIView):

    """
    needs:
    \n- username("phone") and password
    """

    def post(self, request, *args, **kwargs):
        user = authenticate(phone=request.data['username'], password=request.data['password'])
        if user:
            res = get_token(request.data['username'], request.data['password'])
            return Response(res)
        return Response('username or password is incorrect')


class UserLogOutView(APIView):

    """
    we'll get token from "Authorization" field in headers
    \n no need to send anything
    """

    def post(self, request):
        token = request.headers.get('Authorization')
        return Response(logout_user(token))
