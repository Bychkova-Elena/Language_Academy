from .models import UserProfile
from django.contrib.auth.models import User

class UserValidators:
    @staticmethod
    def isUserExists(username):
        return User.objects.filter(username=username).exists()

    @staticmethod
    def isValidUserRole(role):
        return role in UserProfile.ROLE