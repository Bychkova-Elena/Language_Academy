
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Homework, TimeTable
from .serializers import (CourseSerializer, HomeworkByCourseSerializer,
                          TimeTableByCourseSerializer)


class GetCorseView(APIView):
    def get(self):
        '''Вывод групп пользователя'''
        try:
            user = self.request.user

            courses = Course.objects.filter(student__user=user)
            courses = CourseSerializer(courses, many=True)

            return Response({ 'courses': courses.data})

        except Exception as error:
            return Response(
                data={'error': str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetTimeTableView(APIView):
    def get(self, request, pk):
        try:
            timetable = TimeTable.objects.filter(course=pk)
            serializer = TimeTableByCourseSerializer(timetable, many=True)

            return Response({ 'timetable': serializer.data})

        except Exception as error:
            return Response(
                data={'error': str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetHomeworkView(APIView):
    def get(self, request, pk):
        try:
            homework = Homework.objects.filter(course=pk)
            serializer = HomeworkByCourseSerializer(homework, many=True)

            return Response(data={'homeworks': serializer.data})

        except Exception as error:
            return Response(
                data={'error': str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
