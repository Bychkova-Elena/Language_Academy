from rest_framework import serializers
from .models import Level
from users.models import Teacher

class LevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Level
        fields = ("name", )
        
class LanguageTeachersSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Teacher
        fields = ('language', )
        
        