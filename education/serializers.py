from rest_framework import serializers

from .models import Course, Homework, TimeTable


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class AddCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("name", "language", "level", "teacher")


class UpdateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class AllHomeworksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Homework
        fields = '__all__'

class HomeworkSerializer(serializers.ModelSerializer):
    # домашнее задание группы #

    class Meta:
        model = Homework
        exclude = ("course", )

class AddHomeworkSerializer(serializers.ModelSerializer):
    # добавление дз группы #

    class Meta:
        model = Homework
        fields = ("name", "link", "description", "deadline", "onEveryLesson", "course", "draft" )

class UpdateHomeworkSerializer(serializers.ModelSerializer):
    # редактирование дз #

    class Meta:
        model = Homework
        fields = ("name", "link", "description", "deadline", "onEveryLesson", "draft" )

class TimeTableByCourseSerializer(serializers.ModelSerializer):
    # расписание по группе #

    class Meta:
        model = TimeTable
        exclude = ("course", )
