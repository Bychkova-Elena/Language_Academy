from rest_framework import serializers

from .models import Course, Homework, TimeTable


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'level', 'language', 'price', 'students')


class AddCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ("students", "id")


class UpdateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
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
        exclude = ("created", "id" )

class UpdateHomeworkSerializer(serializers.ModelSerializer):
    # редактирование дз #

    class Meta:
        model = Homework
        exclude = ("created", "id", "course" )

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
