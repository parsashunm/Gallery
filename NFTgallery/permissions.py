from rest_framework.permissions import BasePermission


class IsSpecificUser(BasePermission):
    def has_permission(self, request, view):
        user_id = view.kwargs.get('user_id')
        return request.user.id == int(user_id) and request.user
