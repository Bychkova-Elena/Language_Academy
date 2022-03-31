from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError

from users.validators import UserValidators
from core.validators import RequestValidator
from users.models import UserProfile, Teacher, Student

from .jwt_tokens import JWTTokens
from .serializers import  UserSerializer

class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        try:
            data = request.data

            if not RequestValidator(request).containNotEmpty(fields=['username', 'password', 'role']):
                return Response(data={'error': 'Недостаточно данных для регистрации'}, status=status.HTTP_400_BAD_REQUEST)

            username = data['username']
            password = data['password']
            role = data['role']

            if not UserValidators.isValidUsername(username=username):
                return Response(data={'error': 'Имя пользователя является недопустимым'}, status=status.HTTP_400_BAD_REQUEST)

            if not UserValidators.isValidPassword(password=password):
                return Response(data={'error': 'Пароль является недопустимым'}, status=status.HTTP_400_BAD_REQUEST)

            if not UserValidators.isValidUserRole(role=role):
                return Response(data={'error': 'Роль пользователя является недопустимой'}, status=status.HTTP_400_BAD_REQUEST)

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
    
    def post(self, request):
        try:
            response = Response(status=status.HTTP_200_OK)

            data = request.data

            if not RequestValidator(request).containNotEmpty(fields=['username', 'password']):
                return Response(data={ 'error': 'Недостаточно данных для авторизации' }, status=status.HTTP_400_BAD_REQUEST)

            username = data['username']
            password = data['password']

            user = authenticate(username=username, password=password)

            if user is None or not user.is_active:
                return Response(data={ 'error': 'Неверный логин или пароль' }, status=status.HTTP_400_BAD_REQUEST)

            tokens = JWTTokens.getTokensByUser(user=user)

            JWTTokens.addTokensToResponse(response=response, tokens=tokens)

            return response

        except Exception as error:
            return Response(data={ 'error': str(error) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            response = Response(status=status.HTTP_200_OK)

            refreshToken = request.COOKIES.get(JWTTokens.REFRESH_TOKEN_KEY)

            if refreshToken is None:
                return Response(data={ 'error': 'Не авторизован' }, status=status.HTTP_401_UNAUTHORIZED)

            JWTTokens.outdateTokens(refreshToken=refreshToken)
            response.delete_cookie(JWTTokens.REFRESH_TOKEN_KEY)

            return response

        except TokenError:
            return Response(data={ 'error': 'Не авторизован' }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as error:
            return Response(data={ 'error': str(error) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TokenRefreshView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            response = Response(status=status.HTTP_201_CREATED)
        
            refreshToken = request.COOKIES.get(JWTTokens.REFRESH_TOKEN_KEY)

            if refreshToken is None:
                return Response(data={ 'error': 'Не авторизован' }, status=status.HTTP_401_UNAUTHORIZED)

            newTokens = JWTTokens.getNewTokens(refreshToken)
            JWTTokens.addTokensToResponse(response, newTokens)

            return response

        except TokenError:
            return Response(data={ 'error': 'Не авторизован' }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as error:
            return Response(data={ 'error': str(error) }, status=status.HTTP_400_BAD_REQUEST)

class DeleteAccountView(APIView):
    def delete(self):
        try:
            user = self.request.user

            User.objects.filter(id=user.id).delete()

            return Response(status=status.HTTP_200_OK)

        except Exception as error:
            return Response({ 'error': str(error) }, status=status.HTTP_400_BAD_REQUEST)


class GetUsersView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        try:
            users = User.objects.all()

            users = UserSerializer(users, many=True, format=format)

            return Response(data=users.data, status=status.HTTP_200_OK)
            
        except Exception as error:
            return Response(data={ 'error': str(error) }, status=status.HTTP_400_BAD_REQUEST)
