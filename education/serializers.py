from rest_framework import serializers

from .models import Course, Homework, TimeTable


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'level',  'language', 'price', 'student')

class TimeTableByCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        exclude = ("course", )

class HomeworkByCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        exclude = ("course", )
