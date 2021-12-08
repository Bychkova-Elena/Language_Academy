from rest_framework import fields, serializers

from .models import Course, Homework, TimeTable

class TimeTableByCourseSerializer(serializers.ModelSerializer):
    # расписание по группе #

    class Meta:
        model = TimeTable
        exclude = ("course", )