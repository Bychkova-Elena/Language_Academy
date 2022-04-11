from django.shortcuts import render
from .models import Level
from rest_framework import permissions
from .serializers import  LevelSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class LevelView(APIView):
  
    permission_classes=[permissions.AllowAny] 
    
    def get(self, request, format=None):
        '''Вывод уровней'''
    
        try:
            
            levels = Level.objects.all()
              
            levels = LevelSerializer(levels, many=True)

            return Response({ 'Level': levels.data})
            
        except:
          return Response({ 'error': 'Something went wrong when retrieving levels' })
