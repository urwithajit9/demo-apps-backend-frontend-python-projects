from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to the owner of the object.
        return obj.created_by == request.user


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow staff members to modify objects.
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to staff members.
        return request.user.is_staff


class IsQuizOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a quiz to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to the owner of the quiz.
        return obj.created_by == request.user


class IsQuizResponseOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a quiz response to view or edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Permissions are only allowed to the owner of the quiz response.
        return obj.user == request.user
