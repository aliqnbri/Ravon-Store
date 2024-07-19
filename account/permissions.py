from rest_framework import permissions


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