from django.contrib import admin

from .models import Course, Homework, TimeTable


class TimeTableInline(admin.StackedInline):
    model = TimeTable
    extra = 0
    
class HomeworkInline(admin.StackedInline):
    model = Homework
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
  list_display = ("name", "language", "level", "teacher")
  list_filter = ("language", "level", "teacher__user")
  search_fields = ("name", "teacher__user__username")
  inlines = [TimeTableInline, HomeworkInline]
  save_on_top = True
  save_as = True
  fieldsets = (
        (None, {
            "fields": (("name", "teacher", "price"),)
        }),
        (None, {
            "fields": (("language", "level"),)
        }),
        (None, {
            "fields": ("student", )
        })
    )
  
@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
  list_display = ("name", "course", "url", "created", "deadline", "durable")
  list_filter = ("durable", )
  search_fields = ("name", "course__name")
  save_as = True
  list_editable = ("durable",)
  fieldsets = (
        (None, {
            "fields": (("name", "url"),)
        }),
        (None, {
            "fields": ("descrition", "durable", "course")
        }),
        (None, {
            "fields": (("created", "deadline"),)
        })
    )
  
@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
  list_display = ("course", "time")
  search_fields = ("course__name", )
  

