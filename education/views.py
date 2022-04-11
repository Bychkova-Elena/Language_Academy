from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import status
from rest_framework import permissions

from language_academy.users.models import Teacher
from .permissions import TeachersOnly
from .models import Course, Homework, TimeTable
from .serializers import TimeTableByCourseSerializer, HomeworkByCourseSerializer, CourseSerializer, AddCourseSerializer, UpdateCourseSerializer
from rest_framework.views import APIView
from rest_framework.response import response

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
        
class TeachersCourseView(APIView):
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
        
    def post(self, request):
        '''Добавление группы'''
    
        try:
            
            user = self.request.user
            teacher = Teacher.objects.filter(user=user)
            data = {
              'name': request.data['name'],
              'language': request.data['language'],
              'level': request.data['level'],
              'price': request.data['price'], 
              'teacher': teacher.id
            }
             
            if TeachersOnly.has_object_permission(user):
              
                course = AddCourseSerializer(data = data)
                if course.is_valid():
                    course.save()
                return Response({ 'Course': course.data})
            else:
              return Response({ 'error': 'Not a teacher' })
          
        except:
          return Response({ 'error': 'Something went wrong when additing courses' })

      
class UpdateDeleteCorseView(APIView):
    permission_classes=[permissions.IsAuthenticated, TeachersOnly]   
      
    def put(self, request, courseId=None):
        '''Редактирование групп учителя'''
    
        try:
            
            user = self.request.user
             
            if TeachersOnly.has_object_permission(user):
                
              courses = Course.objects.all()
              courses = get_object_or_404(courses, pk=courseId)
              course = UpdateCourseSerializer(instance=courses, data=request.data)
              if course.is_valid():
                course.save()
              return Response({ 'Course': course.data}) 
            
            else:
              return Response({ 'error': 'Not a teacher' })
        except:
          return Response({ 'error': 'Something went wrong when updating courses' })
        
    def delete(self, request, courseId=None):
        '''Удаление групп учителя'''
    
        try:
            
            user = self.request.user
             
            if TeachersOnly.has_object_permission(user):
                
              courses = Course.objects.all()
              course = get_object_or_404(courses, pk=courseId)
              course.delete()
              return Response(status=200)
            
            
            else:
              return Response({ 'error': 'Not a teacher' })
        except:
          return Response({ 'error': 'Something went wrong when updating courses' })
    
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
