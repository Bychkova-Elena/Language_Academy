from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import status
from rest_framework import permissions

from language_academy.users.models import Teacher
from .permissions import TeachersOnly
from .models import Course, Homework, TimeTable
from .serializers import TimeTableByCourseSerializer, HomeworkByCourseSerializer, CourseSerializer, AddCourseSerializer, UpdateCourseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import Teacher, UserProfile
from rest_framework import status
        
class GetCourseView(APIView):
    permission_classes=[permissions.IsAuthenticated, TeachersOnly] 
    
    def get(self, request, format=None):
        '''Вывод групп'''
    
        try:
            
            user = self.request.user
            userprofile = UserProfile.objects.get(user=user)
            params = self.request.query_params

            limit = params.get('limit', None)
            skip = params.get('skip', None)
            
            if userprofile.role == "STUDENT":
                 courses = Course.objects.filter(student__user=user)
            else:
            
              courses = Course.objects.filter(teacher__user=user) 
              
            if skip: 
              courses = courses[int(skip):]
            
            if limit:
              courses = courses[:int(limit)]
            
            courses = CourseSerializer(courses, many=True)

            return Response(courses.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(data={ 'error': str(error) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        '''Добавление группы'''
    
        try:
            
            user = self.request.user
            teacher = Teacher.objects.get(user=user)
            data = {
              'name': request.data['name'],
              'language': request.data['language'],
              'level': request.data['level'],
              'price': request.data['price'], 
              'teacher': teacher.id
            }
              
            course = AddCourseSerializer(data = data)
            if course.is_valid():
                    course.save()
            return Response(course.data, status=status.HTTP_201_CREATED)
          
        except Exception as error:
            return Response(data={ 'error': str(error) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

      
class UpdateDeleteCorseView(APIView):
    permission_classes=[permissions.IsAuthenticated, TeachersOnly]   
      
    def put(self, request, courseId=None):
        '''Редактирование групп учителя''' 
    
        try:
             
            if TeachersOnly.has_object_permission(self, request):
              
              courses = Course.objects.get(pk=courseId)
              course = UpdateCourseSerializer(instance=courses, data=request.data)
              if course.is_valid():
                course.save()
              return Response(course.data, status=status.HTTP_200_OK) 
            
            else:
              return Response({ 'error': 'Не учитель' }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(data={ 'error': str(error) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, courseId=None):
        '''Удаление групп учителя'''
        
        try:
             
            if TeachersOnly.has_object_permission(self, request):
                
              course = Course.objects.get(pk=courseId)
              course.delete()
              return Response(status=status.HTTP_200_OK)
            
            
            else:
              return Response({ 'error': 'Не учитель' }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(data={ 'error': str(error) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
            
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        except Exception as error:
            return Response(data={ 'error': str(error) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
