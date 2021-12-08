from django.shortcuts import render

from .models import Course, Homework, TimeTable
from .serializers import TimeTableByCourseSerializer

from rest_framework import viewsets
from rest_framework.response import Response

def index(request):
  return render(request, 'index.html', {})

class TimeTableView(viewsets.ViewSet):
  
    def list(self, request, pk):
        '''Вывод расписания группы'''

        timetable = TimeTable.objects.filter(course=pk)
        serializer = TimeTableByCourseSerializer(timetable, many=True)
        return Response(serializer.data)

