from rest_framework import permissions
from typing import Any
from django.db.models.signals import pre_save
from django.dispatch import receiver
from account.models import CustomUser


class BaseIsAuthenticated(permissions.BasePermission):
    """
    Base permission class that checks if the user is authenticated.
    All other permission classes can inherit from this class.
    """
    def has_permission(self, request, view)-> bool:
        return request.user.is_authenticated
    
class IsOwner(BaseIsAuthenticated):
    """
    Permission class that allows access only if the user is the owner of the object.
    Inherits from BaseIsAuthenticated to avoid repeating the authentication check.
    """
    def has_object_permission(self, request, view, obj) -> bool:
        return obj.user == request.user
    
class IsOwnerOrReadOnly(BaseIsAuthenticated):
    """
    Permission class that allows read-only access to all users,
    but write access only to the owner of the object.
    Inherits from BaseIsAuthenticated.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user    
    
class IsAdmin(BaseIsAuthenticated):
    """
    Permission class that allows access only to admin users.
    Inherits from BaseIsAuthenticated.
    """

    def has_permission(self, request, view) -> bool:
        return super().has_permission(request, view) and request.user.role == CustomUser.Role.ADMIN


class IsStaff(BaseIsAuthenticated):
    """
    Permission class that allows access only to staff users.
    Inherits from BaseIsAuthenticated.
    """

    def has_permission(self, request, view) -> bool:
        return super().has_permission(request, view) and request.user.role == CustomUser.Role.STAFF


class IsCustomer(BaseIsAuthenticated):
    """
    Permission class that allows access only to customer users.
    Inherits from BaseIsAuthenticated.
    """

    def has_permission(self, request, view) -> bool:
        return super().has_permission(request, view) and request.user.role == CustomUser.Role.CUSTOMER    



class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class IsAnonymous(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_anonymous


# get user role number and set instance privileges for that role in pre_save signal
def get_set_role(user_instance):
    match user_instance.role:
        case 'ADMIN':
            user_instance.is_staff = True
            user_instance.is_superuser = True
            user_instance.staff_role = None
            return "ADMIN"
        case 'STAFF':
            user_instance.is_staff = True
            user_instance.is_superuser = False
            return "STAFF"
        case 'CUSTOMER':
            user_instance.is_staff = False
            user_instance.is_superuser = False
            user_instance.staff_role = None
            return "CLIENT"
        case _:
            return "Invalid role ID"