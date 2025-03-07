# from django.shortcuts import render, get_object_or_404
import random

from django.shortcuts import redirect
from rest_framework.views import APIView, Response
from rest_framework.generics import CreateAPIView, UpdateAPIView
from django.contrib.auth import authenticate

from permissions import IsArtist
from utils import send_otp
#
from .serializers import CreateAccountSerializer, ConfirmOtpCodeSerializer, UserLoginSerializer, UserProfileSerializer, \
    UserEditProfileSerializer
from .models import User, OTP, UserProfile
from accounts.oAuth import get_token, logout_user
#


class UserCreateView(APIView):
    """
    needs:
    \n- username/phone/password/pass2(confirm password)
    """

    serializer_class = CreateAccountSerializer

    def post(self, request):
        ser_data = CreateAccountSerializer(data=request.data)
        if ser_data.is_valid():
            cd = ser_data.validated_data
            code = str(random.randint(10000, 99999))
            OTP.objects.create(phone=cd['phone'], code=code)
            send_otp(cd['phone'], code)
            request.session['user_registration_info'] = {
                'username': cd['username'],
                'phone': cd['phone'],
                'password': cd['password']
            }
            return Response({"detail": 'OTP sent'})
        return Response(ser_data.errors)


class ConfirmOtpView(APIView):

    """
    you should send the code that we sent to user phone number
    """

    serializer_class = ConfirmOtpCodeSerializer

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        user_session = request.session['user_registration_info']
        code_instance = OTP.objects.filter(phone=user_session['phone']).last()

        if srz_data.is_valid():
            vd = srz_data.validated_data
            if code_instance.expire_code():
                return Response({"error": 'code have been expired'})
            if str(code_instance.code) == vd['code']:
                User.objects.create(username=user_session['username'], phone=user_session['phone'],
                                    password=user_session['password'])
                code_instance.delete()
                return Response({"detail": 'you registered successfully'})
        return Response({"error": "the code that you entered was wrong"})


class UserLoginView(APIView):

    """
    needs:
    \n- username("phone") and password
    """

    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):

        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            vd = srz_data.validated_data
            user = authenticate(phone=vd['username'], password=vd['password'])
            if user:
                res = get_token(request, request.data['username'], request.data['password'])
                return Response(res)
        return Response({'error': 'username or password is incorrect'})


class UserLogOutView(APIView):

    """
    we'll get token from "Authorization" field in headers
    \n no need to send anything
    """
    serializer_class = None

    def post(self, request):
        token = request.headers.get('Authorization').split()[1]
        return Response(logout_user(request, token))


class CreateUserProfileView(CreateAPIView):
    permission_classes = [IsArtist]
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class UserEditProfileView(UpdateAPIView):
    """
        only request with PATCH method
    """
    permission_classes = [IsArtist]
    serializer_class = UserEditProfileSerializer
    queryset = UserProfile.objects.all()
    lookup_field = 'user'
