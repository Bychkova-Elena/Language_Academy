from .models import UserProfile
from django.contrib.auth.models import User

class UserValidators:
    USERNAME_MIN_LENGTH = 6
    USERNAME_ACCEPTED_SYMBOLS = "abcdefghijklmnopqrstuvwxyz0123456789-_.@"
    PASSWORD_MIN_LENGTH = 6

    def isUserExists(username) -> bool:
        return User.objects.filter(username=username).exists()

    def isValidUserRole(role) -> bool:
        return role in [UserProfile.STUDENT, UserProfile.TEACHER]

    def isValidUsername(username) -> bool:
        if len(username) < UserValidators.USERNAME_MIN_LENGTH:
            return False

        if not all(s in UserValidators.USERNAME_ACCEPTED_SYMBOLS for s in username):
            return False

        return True

    def isValidPassword(password) -> bool:
        if len(password) < UserValidators.PASSWORD_MIN_LENGTH:
            return False

        return True