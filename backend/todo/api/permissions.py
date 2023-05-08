from rest_framework.permissions import BasePermission


class IsOwnerOrSuperUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        grant permission if the user is the owner of the task or is a superuser
        """
        return bool(request.user.is_authenticated and
                    obj.author == request.user or
                    request.user.is_superuser
                    )


class IsVerified(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_verified)
