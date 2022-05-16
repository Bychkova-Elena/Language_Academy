from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from education.models import Course
from .models import UserProfile
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import UserProfileSerializer, StudentsSerializer

class UserProfileListCreateView(ListCreateAPIView):
    queryset=UserProfile.objects.all()
    serializer_class=UserProfileSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        '''Создание пользователя'''
        user=self.request.user
        serializer.save(user=user)

class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset=UserProfile.objects.all()
    serializer_class=UserProfileSerializer
    permission_classes=[IsOwnerProfileOrReadOnly,permissions.IsAuthenticated]

class StudentsView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request, courseId=None):
        '''Вывод учеников курса'''

        try:
            course = Course.objects.get(pk=courseId)
            students = StudentsSerializer(course)

            return Response(students.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(data={ 'error': str(error) },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
