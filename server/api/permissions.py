from rest_framework import permissions

from .models import Template


class IsOwner(permissions.BasePermission):
    """ Custom permission class to allow only Template owners to edit them.
    """

    def has_object_permission(self, request, view, obj):
        """ Return True id permission is granted to the template owner
        """
        if isinstance(obj, Template):
            return obj.owner == request.user
        return obj.owner == request.user
