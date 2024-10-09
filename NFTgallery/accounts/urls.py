from django.urls import path, include
#
from .views import (UserLoginView, UserLogOutView, UserCreateView, ConfirmOtpView)
#

urlpatterns = [
    path('user/register/', UserCreateView.as_view(), name='user_register'),
    path('user/register/confirm/', ConfirmOtpView.as_view(), name='confirm_code'),
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    path('user/logout/', UserLogOutView.as_view(), name='user_logout'),
]
