from django.urls import path, include
#
from .views import UserLoginView, UserLogOutView, UserCreateView
#

app_name = 'accounts'

urlpatterns = [
    path('user/register/', UserCreateView.as_view(), name='user_register'),
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    path('user/logout/', UserLogOutView.as_view(), name='user_logout'),
]
