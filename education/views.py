from django.shortcuts import render

from .models import Course, Homework, TimeTable
from .serializers import TimeTableByCourseSerializer, HomeworkByCourseSerializer

from rest_framework import viewsets
from rest_framework.response import Response

class TimeTableView(viewsets.ViewSet):
  
    def list(self, request, pk):
        '''Вывод расписания группы'''

        timetable = TimeTable.objects.filter(course=pk)
        serializer = TimeTableByCourseSerializer(timetable, many=True)
        return Response(serializer.data)
      
class HomeworkView(viewsets.ViewSet):
  
    def list(self, request, pk):
        '''Вывод домашних заданий группы'''

        homework = Homework.objects.filter(course=pk)
        serializer = HomeworkByCourseSerializer(homework, many=True)
        return Response(serializer.data)


