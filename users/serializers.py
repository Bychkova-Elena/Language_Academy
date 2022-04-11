from rest_framework import serializers
from .models import UserProfile, Teacher

class userProfileSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'
        
class LanguageTeachersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = fields = ('language', )
        