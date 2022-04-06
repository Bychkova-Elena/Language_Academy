from rest_framework import permissions
from users.models import Teacher
    
class TeachersOnly(permissions.BasePermission):
    
    def has_object_permission(user):
        
        return Teacher.objects.filter(user = user).exists()