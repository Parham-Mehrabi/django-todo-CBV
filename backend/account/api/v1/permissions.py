from rest_framework.permissions import BasePermission


class IsNotVerifiedOrNotLogin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_verified:
            return False
        return True
