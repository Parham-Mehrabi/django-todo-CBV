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
