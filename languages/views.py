from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from users.models import Teacher
from .models import Level, Language
from .serializers import  LevelSerializer, LanguageTeachersSerializer

class LevelView(APIView):

    permission_classes=[permissions.AllowAny]

    def get(self, request):
        '''Вывод уровней'''

        try:

            levels = Level.objects.all()

            levels = LevelSerializer(levels, many=True)

            return Response(levels.data, status=status.HTTP_200_OK)

        except Exception as error:
            return Response(data={ 'error': str(error) },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LanguageTeachersView(APIView):
    permission_classes=[permissions.AllowAny]

    def get(self, request):
        '''Вывод преподаваемых языков'''

        try:

            user = self.request.user

            user = Teacher.objects.get(user=user)

            language = Language.objects.filter(pk__in=user.language.all())

            language = LanguageTeachersSerializer(language, many=True)

            return Response(language.data, status=status.HTTP_200_OK)

        except Exception as error:
            return Response(data={ 'error': str(error) },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
