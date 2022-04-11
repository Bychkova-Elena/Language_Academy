from django.shortcuts import render
from .models import Level
from rest_framework import permissions
from .serializers import  LevelSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class LevelView(APIView):
  
    permission_classes=[permissions.AllowAny] 
    
    def get(self, request, format=None):
        '''Вывод уровней'''
    
        try:
            
            levels = Level.objects.all()
              
            levels = LevelSerializer(levels, many=True)

            return Response({ 'Level': levels.data}, status=status.HTTP_200_OK)
            
        except Exception as error:
            return Response({ 'error': str(error) }, status=status.HTTP_400_BAD_REQUEST)
