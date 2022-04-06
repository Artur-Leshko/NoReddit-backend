from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsPostOwner(BasePermission):
    '''
        Owner of the post
    '''
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and obj.owner.id == request.user.id
