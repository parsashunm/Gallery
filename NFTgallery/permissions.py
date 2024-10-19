from rest_framework.permissions import BasePermission

from accounts.models import User


class IsSpecificUser(BasePermission):
    def has_permission(self, request, view):
        user_id = view.kwargs.get('user_id')
        return request.user.id == int(user_id) and request.user


class IsPresenter(BasePermission):
    def has_permission(self, request, view):
        # user = User.objects.get(pk=int(view.kwargs.get('user_id')))
        user = request.user
        if user.is_authenticated:
            return user.role.title == 'presenter' or user.is_admin
        return False


class IsArtist(BasePermission):
    def has_permission(self, request, view):
        # user = User.objects.get(pk=int(view.kwargs.get('user_id')))
        user = request.user
        if user.is_authenticated:
            return user.role.title == 'artist' or user.is_admin
        return False
