from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework import permissions
from core.validators import RequestValidator

from users.validators import UserValidators
from .serializers import  UserSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from users.models import UserProfile, Teacher, Student
from .utils import JWTTokens

class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        try:
            data = request.data

            if not RequestValidator.checkFieldsInRequest(data, ['username', 'password', 'role']):
                return Response(data={'error': 'Недостаточно данных для регистрации'}, status=status.HTTP_400_BAD_REQUEST)

            username = data['username']
            password = data['password']
            role = data['role']

            if not UserValidators.isValidUserRole(role=role):
                return Response(data={'error': 'Предоставленная роль не является допустимой'}, status=status.HTTP_400_BAD_REQUEST)

            if UserValidators.isUserExists(username=username):
                return Response(data={'error': 'Пользователь уже существует'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.create_user(username=username, password=password)

            user_profile = UserProfile.objects.get(user=user)
            user_profile.role = role
            user_profile.save()

            if role == "STUDENT":
                Student.objects.create(user=user)
            else:
                Teacher.objects.create(user=user)

            return Response(status=status.HTTP_201_CREATED)

        except Exception as error:
            return Response(data={ 'error': str(error) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request, format=None):
        try:
            response = Response()

            data = request.data

            if not RequestValidator.checkFieldsInRequest(data, ['username', 'password']):
                return Response(data={'error': 'Недостаточно данных для авторизации'}, status=status.HTTP_400_BAD_REQUEST)

            username = data['username']
            password = data['password']

            user = authenticate(username=username, password=password)

            if user is None or not user.is_active:
                return Response(data={ 'error': 'Пользователь не найден' }, status=status.HTTP_400_BAD_REQUEST)

            tokens = JWTTokens().getTokenForUser(user=user)

            JWTTokens().setTokensToResponse(response=response, tokens=tokens)

        except Exception as error:
            return Response(data={ 'error': str(error) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            response = Response()
            refresh_token = request.COOKIES.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            response.delete_cookie('refresh_token')

            return response
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            response = Response()
        
            refreshToken = request.COOKIES.get(JWTTokens.REFRESH_TOKEN_KEY)

            newTokens = JWTTokens.updateTokens(refreshToken)
            JWTTokens.setTokensToResponse(response, newTokens)

            return response

        except Exception as error:
            print(error)
            return Response({ 'error': str(error) }, status=status.HTTP_400_BAD_REQUEST)




class DeleteAccountView(APIView):
    def delete(self, request, format=None):
        user = self.request.user

        try:
            User.objects.filter(id=user.id).delete()

            return Response({'success': 'User deleted successfully'})
        except:
            return Response({'error': 'Something went wrong when trying to delete user'})


class GetUsersView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        users = User.objects.all()

        users = UserSerializer(users, many=True, format=format)
        return Response({'users': users.data})
