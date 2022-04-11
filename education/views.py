from rest_framework import permissions
from .permissions import TeachersOnly
from .models import Course, Homework, TimeTable
from .serializers import TimeTableByCourseSerializer, HomeworkByCourseSerializer, CourseSerializer, AddCourseSerializer, UpdateCourseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import Teacher
from django.shortcuts import get_object_or_404

class GetCorseView(APIView):
  
    def get(self, request, format=None):
        '''Вывод групп пользователя'''
        try:
            user = self.request.user
            
            courses = Course.objects.filter(student__user=user)
               
            courses = CourseSerializer(courses, many=True)

            return Response({ 'courses': courses.data})
        except:
            return Response({ 'error': 'Something went wrong when retrieving courses' })
        
class TeachersCorseView(APIView):
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
             
            if TeachersOnly.has_object_permission(user): 

                course = AddCourseSerializer(teacher = teacher, data=request.data)
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
  
    def get(self, request, pk):
        '''Вывод расписания группы'''
        
        try:

          timetable = TimeTable.objects.filter(course=pk)
          serializer = TimeTableByCourseSerializer(timetable, many=True)
          return Response({ 'timetable': serializer.data})
        except:
            return Response({ 'error': 'Something went wrong when retrieving timetable' })
        
      
class GetHomeworkView(APIView):
  
    def get(self, request, pk):
        '''Вывод домашних заданий группы'''
        
        try:

          homework = Homework.objects.filter(course=pk)
          serializer = HomeworkByCourseSerializer(homework, many=True)
          return Response({ 'homeworks':serializer.data})
    
        except:
            return Response({ 'error': 'Something went wrong when retrieving homework' })


