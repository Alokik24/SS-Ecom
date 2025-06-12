from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role', None) == 'admin' and request.user.is_authenticated

class IsVendor(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role', None) == 'vendor' and request.user.is_authenticated

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'role', None) == 'customer' and request.user.is_authenticated