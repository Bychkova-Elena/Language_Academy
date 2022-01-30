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
  list_display = ("name", "course", "url", "created", "deadline", "durable", "draft")
  list_filter = ("durable", "draft")
  list_editable = ("draft",)
  search_fields = ("name", "course__name")
  actions = ["publish", "unpublish"]
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

  publish.short_description = "Publish"
  publish.allowed_permissions = ('change', )
  
  unpublish.short_description = "Unpublish"
  unpublish.allowed_permissions = ('change',)
  
@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
  list_display = ("course", "time")
  search_fields = ("course__name", )
  

