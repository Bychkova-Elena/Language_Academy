from rest_framework import serializers
from .models import Level, Language

class LevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Level
        fields = ("name", )

class LanguageTeachersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'
        