from rest_framework import permissions
from users.models import Teacher
    
class TeachersOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            
            return Teacher.objects.filter(user = request.user).exists()
    