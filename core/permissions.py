from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
    Custom permission to only allow superusers.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
