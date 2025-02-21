from django.urls import path
#
from .views import (UserLoginView, UserLogOutView, UserCreateView, ConfirmOtpView, CreateUserProfileView,
                    UserEditProfileView)
#

urlpatterns = [
    path('user/register/', UserCreateView.as_view(), name='user_register'),
    path('user/register/confirm/', ConfirmOtpView.as_view(), name='confirm_code'),
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    path('user/logout/', UserLogOutView.as_view(), name='user_logout'),
    # path('user/profile/create/', CreateUserProfileView.as_view(), name="profile_create"),
    path('user/profile/edit/<int:user>/', UserEditProfileView.as_view(), name="profile_edit"),
]
