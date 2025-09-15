# permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
 
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        return obj.owner == request.user

class IsAdminOrSelf(permissions.BasePermission):
   
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user