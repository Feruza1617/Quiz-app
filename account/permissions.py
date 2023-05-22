from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthenticated(permissions.IsAuthenticated):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_active)

