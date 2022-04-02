from django.shortcuts import render

from .models import Course, Homework, TimeTable
from .serializers import TimeTableByCourseSerializer, HomeworkByCourseSerializer, CourseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

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


