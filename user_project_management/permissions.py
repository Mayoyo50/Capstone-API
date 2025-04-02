from rest_framework.permissions import BasePermission

class IsClient(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user.userprofile, 'client')

class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user.userprofile, 'supervisor')

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user.userprofile, 'student')

class IsAdminOrSupervisor(BasePermission):
    def has_permission(self, request, view):
        profile = request.user.userprofile
        return profile.role == 'ADMIN' or hasattr(profile, 'supervisor')