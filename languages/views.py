from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from users.models import Teachers
from .models import Level
from .serializers import  LevelSerializer, LanguageTeachersSerializer

class LevelView(APIView):

    permission_classes=[permissions.AllowAny]

    def get(self, request):
        '''Вывод уровней языка'''

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
        '''Вывод преподаваемых учителем языков'''

        try:

            user = self.request.user

            language = Teachers.objects.filter(user=user)

            language = LanguageTeachersSerializer(language, many=True)

            return Response(language.data, status=status.HTTP_200_OK)

        except Exception as error:
            return Response(data={ 'error': str(error) },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
