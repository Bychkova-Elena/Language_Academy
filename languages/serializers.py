from rest_framework import serializers
from .models import Level, Language

class LevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Level
        fields = '__all__'

class LanguageTeachersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'
        