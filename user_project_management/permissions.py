from rest_framework.permissions import BasePermission

class CanCreateProject(BasePermission):
    message = "You don't have permission to create projects."

    def has_permission(self, request, view):
        # Only allow authenticated users to create projects
        return request.user.is_authenticated