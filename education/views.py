from rest_framework import status
from rest_framework import permissions
from .permissions import TeachersOnly
from .models import Course, Homework, TimeTable
from .serializers import TimeTableByCourseSerializer, HomeworkByCourseSerializer, CourseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Homework, TimeTable
from .serializers import (CourseSerializer, HomeworkByCourseSerializer,
                          TimeTableByCourseSerializer)


class GetCorseView(APIView):
    @staticmethod
    def get(request):
        '''Вывод групп пользователя'''
        try:
            user = request.user

            courses = Course.objects.filter(student__user=user)
            courses = CourseSerializer(courses, many=True)

            return Response({ 'courses': courses.data})
        except:
            return Response({ 'error': 'Something went wrong when retrieving courses' })
        
class GetTeachersCorseView(APIView):
    permission_classes=[permissions.IsAuthenticated, TeachersOnly] 
    
    def get(self, request, format=None):
        '''Вывод групп учителя'''
    
        try:
            
            user = self.request.user
            params = self.request.query_params

            limit = params.get('limit', None)
            skip = params.get('skip', None)
             
            if TeachersOnly.has_object_permission(user): 
            
              if limit:
                  courses = Course.objects.filter(teacher__user=user)[:int(limit)]
              if skip: 
                  courses = Course.objects.filter(teacher__user=user)[int(skip):]
              else:
                  courses = Course.objects.filter(teacher__user=user)
             
               
              courses = CourseSerializer(courses, many=True)

              return Response({ 'Course': courses.data})
            
            else:
              return Response({ 'error': 'Not a teacher' })
        except:
          return Response({ 'error': 'Something went wrong when retrieving courses' })

class GetTimeTableView(APIView):
    @staticmethod
    def get(pk):
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
    @staticmethod
    def get(pk):
        try:
            homework = Homework.objects.filter(course=pk)
            serializer = HomeworkByCourseSerializer(homework, many=True)

            return Response(data={'homeworks': serializer.data})

        except Exception as error:
            return Response(
                data={'error': str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
