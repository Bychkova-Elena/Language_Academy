from rest_framework import serializers
<<<<<<< HEAD

from .models import UserProfile
=======
from .models import UserProfile, Teacher
>>>>>>> Group: updating and deleting teachers groups


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
<<<<<<< HEAD

    user=serializers.StringRelatedField(read_only=True)
=======
        
class LanguageTeachersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = fields = ('language', )
        
>>>>>>> Group: updating and deleting teachers groups
