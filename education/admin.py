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
  raw_id_fields = ["teacher", "student"]
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
  list_display = ("name", "course", "link", "created", "deadline", "onEveryLesson", "draft")
  list_filter = ("onEveryLesson", "draft")
  list_editable = ("draft",)
  search_fields = ("name", "course__name")
  actions = ["publish", "unpublish"]
  raw_id_fields = ["course", ]
  save_as = True
  list_editable = ("onEveryLesson",)
  fieldsets = (
        (None, {
            "fields": (("name", "link"),)
        }),
        (None, {
            "fields": ("descrition", "onEveryLesson", "course")
        }),
        (None, {
            "fields": (("created", "deadline"),)
        })
    )
  def unpublish(self, request, queryset):
        #Снять с публикации#
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 record was changed"
        else:
            message_bit = f"{row_update} records were changed"
        self.message_user(request, f"{message_bit}")

  def publish(self, request, queryset):
        #Опубликовать#
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 record was changed"
        else:
            message_bit = f"{row_update} records were changed"
        self.message_user(request, f"{message_bit}")

  publish.short_description = "Опубликовать"
  publish.allowed_permissions = ('change', )
  
  unpublish.short_description = "Снять с публикации"
  unpublish.allowed_permissions = ('change',)
  
@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
  list_display = ("course", "starts", "end", "period")
  search_fields = ("course__name", )
  raw_id_fields = ["course", ]
  

