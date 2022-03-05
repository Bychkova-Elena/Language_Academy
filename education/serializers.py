from rest_framework import fields, serializers

from .models import Course, Homework, TimeTable

class CourseSerializer(serializers.ModelSerializer):
    # названия групп пользователя #

    class Meta:
        model = Course
        fields = ('name', )

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