from rest_framework import permissions

# from .models import Template


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ Custom permission class to allow only Template owners to edit them.
    """

    def has_object_permission(self, request, view, obj):
        """ Return True if permission is granted to the template owner or it's
        a read only request to a template.
        """
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
