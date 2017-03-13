#===============================================================================
# Created on 1 déc. 2016
# @author: Matthieu
#===============================================================================

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    """
    Custom permission to only allow ADMIN members to edit objects
    """
    def has_permission(self, request, view):
        
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Python3: is_admin = super().has_permission(request, view)
        is_admin = super(IsAdminOrReadOnly, self).has_permission(request, view)
        
        return is_admin