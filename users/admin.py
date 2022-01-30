from django.contrib import admin
from .models import Teacher, Student, UserProfile

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
  list_display = ("user",)
  list_filter = ("language", )
  search_fields = ("user__username", )
  
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
  list_display = ("user", )
  search_fields = ("user__username", )
  
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
  list_display = ("user",)
  list_filter = ("role", )
  search_fields = ("first_name", "last_name")
