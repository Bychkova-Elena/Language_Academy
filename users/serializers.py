from rest_framework import serializers
from education.models import Course
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'

class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        exclude = ("user", "id", "role")

class StudentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('students', )
        