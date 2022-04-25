from rest_framework import fields, serializers

from .models import Course, Homework, TimeTable

class CourseSerializer(serializers.ModelSerializer):
    # группы #

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
        exclude = ("teacher", "id")

class TimeTableByCourseSerializer(serializers.ModelSerializer):
    # расписание по группе #

    class Meta:
        model = TimeTable
        exclude = ("course", )
        
class HomeworkByCourseSerializer(serializers.ModelSerializer):
    # домашнее задание группы #

    class Meta:
        model = Homework
        exclude = ("course", )