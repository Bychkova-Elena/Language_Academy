from rest_framework import serializers

from languages.models import Language, Level

from .models import Course, Homework, TimeTable


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseInfoSerializer(serializers.ModelSerializer):
    level = LevelSerializer()
    language = LanguageSerializer()

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
    course = CourseSerializer()

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
        fields = ("name", "link", "description", "deadline", "onEveryLesson", "course", "draft")


class UpdateHomeworkSerializer(serializers.ModelSerializer):
    # редактирование дз #

    class Meta:
        model = Homework
        fields = ("name", "link", "description", "deadline", "onEveryLesson", "draft")


class TimeTableByCourseSerializer(serializers.ModelSerializer):
    # расписание по группе #

    class Meta:
        model = TimeTable
        exclude = ("course", )
