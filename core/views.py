from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from users.models import Student, Teacher, UserProfile, UserRole
from users.validators import UserValidators

from core.validators import RequestValidator

from .jwt_tokens import JWTTokens
from .serializers import UserSerializer


class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    @staticmethod
    def post( request):
        try:
            data = request.data

            if (
                not RequestValidator.ContainNotEmpty(
                    data=request.data,
                    fields=['username', 'password', 'role']
                )
            ):
                return Response(
                    data={'error': 'Недостаточно данных для регистрации'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            username = data['username']
            password = data['password']
            role = data['role']

            if not UserValidators.IsValidUsername(username=username):
                return Response(
                    data={'error': 'Имя пользователя является недопустимым'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not UserValidators.IsValidPassword(password=password):
                return Response(
                    data={'error': 'Пароль является недопустимым'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not UserValidators.IsValidUserRole(role=role):
                return Response(
                    data={'error': 'Роль пользователя является недопустимой'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if UserValidators.IsUserExists(username=username):
                return Response(
                    data={'error': 'Пользователь уже существует'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.create_user(username=username, password=password)

            userProfile = UserProfile.objects.create(user=user, role=role)

            if userProfile.role == UserRole.STUDENT:
                Student.objects.create(user=user)
            else:
                Teacher.objects.create(user=user)

            return Response(status=status.HTTP_201_CREATED)

        except Exception as error:
            print(error)
            return Response(
                data={'error': str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    @staticmethod
    def post(request):
        try:
            response = Response(status=status.HTTP_200_OK)

            data = request.data

            if (
                not RequestValidator.ContainNotEmpty(
                    data=request.data,
                    fields=['username', 'password']
                )
            ):
                return Response(
                    data={'error': 'Недостаточно данных для авторизации'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            username = data['username']
            password = data['password']

            user = authenticate(username=username, password=password)

            if user is None or not user.is_active:
                return Response(
                    data={'error': 'Неверный логин или пароль'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            tokens = JWTTokens.GetTokensByUser(user=user)

            JWTTokens.AddTokensToResponse(response=response, tokens=tokens)

            return response

        except Exception as error:
            return Response(
                data={'error': str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request):
        try:
            response = Response(status=status.HTTP_200_OK)

            refreshToken = request.COOKIES.get(JWTTokens.REFRESH_TOKEN_KEY)

            if refreshToken is None:
                return Response(
                    data={'error': 'Не авторизован'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            JWTTokens.OutdateTokens(refreshToken=refreshToken)
            response.delete_cookie(JWTTokens.REFRESH_TOKEN_KEY)

            return response

        except TokenError:
            return Response(
                data={'error': 'Не авторизован'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        except Exception as error:
            return Response(
                data={'error': str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TokenRefreshView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request):
        try:
            response = Response(status=status.HTTP_201_CREATED)

            refreshToken = request.COOKIES.get(JWTTokens.REFRESH_TOKEN_KEY)

            if refreshToken is None:
                return Response(
                    data={'error': 'Не авторизован'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            newTokens = JWTTokens.GetNewTokens(refreshToken)
            JWTTokens.AddTokensToResponse(response, newTokens)

            return response

        except TokenError:
            return Response(
                data={'error': 'Не авторизован'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        except Exception as error:
            return Response(
                data={'error': str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeleteAccountView(APIView):
    @staticmethod
    def delete(request):
        try:
            user = request.user

            User.objects.filter(id=user.id).delete()

            return Response(status=status.HTTP_200_OK)

        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MeView(APIView):
    @staticmethod
    def get(request):
        try:
            user = request.user

            if not user:
                Response(
                    data={'error': 'Невалидный пользователь'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            userProfile = UserProfile.objects.get(user=user)

            if not userProfile:
                Response(
                    data={'error': 'Невалидный пользователь'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                data={
                    'id': user.id,
                    'username': user.username,
                    'role': userProfile.role,
                    'firstName': userProfile.firstName,
                    'lastName': userProfile.lastName,
                },
                status=status.HTTP_200_OK
            )

        except Exception as error:
            return Response(
                data={'error': str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetUsersView(APIView):
    permission_classes = (permissions.AllowAny, )

    @staticmethod
    def get(format=None):
        try:
            users = User.objects.all()

            users = UserSerializer(users, many=True, format=format)

            return Response(data=users.data, status=status.HTTP_200_OK)

        except Exception as error:
            return Response(
                data={'error': str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
