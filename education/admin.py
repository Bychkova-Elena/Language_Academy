from django.contrib import admin

from .models import Course, Homework, TimeTable

admin.site.register(Course)
admin.site.register(Homework)
admin.site.register(TimeTable)
