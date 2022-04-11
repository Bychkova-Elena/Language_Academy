from rest_framework import serializers

from .models import Course, Homework, TimeTable

<<<<<<< HEAD
=======
class CourseSerializer(serializers.ModelSerializer):
    # группы #
>>>>>>> Group: updating and deleting teachers groups

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'level',  'language', 'price', 'student')
        
class AddCourseSerializer(serializers.ModelSerializer):
    # добавление групп #

    class Meta:
        model = Course
        exclude = ("student", )
        
class UpdateCourseSerializer(serializers.ModelSerializer):
    # редактирование групп #

    class Meta:
        model = Course
        fields = ('name', 'level',  'language', 'price', 'student' )

class TimeTableByCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        exclude = ("course", )

class HomeworkByCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        exclude = ("course", )
