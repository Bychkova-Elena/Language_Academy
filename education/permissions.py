from rest_framework import permissions
from users.models import Teachers

class TeachersOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:

            return Teachers.objects.filter(user = request.user).exists()


        return None
