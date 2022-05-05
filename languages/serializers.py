from rest_framework import serializers
from users.models import Teacher
from .models import Level

class LevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Level
        fields = ("name", )

class LanguageTeachersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ('language', )
        