from rest_framework import permissions

class IsTeacher(permissions.BasePermission):
    """
    Разрешение, которое позволяет доступ только учителям.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_teacher)

class IsAdmin(permissions.BasePermission):
    """
    Разрешение, которое позволяет доступ только администраторам.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)