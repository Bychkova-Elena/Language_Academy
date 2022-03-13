from django.contrib import admin
from .models import Teacher, Student, UserProfile

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
  list_display = ("user",)
  list_filter = ("language", )
  search_fields = ("user__username", )
  raw_id_fields = ["user", ]
  
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
  list_display = ("user", )
  search_fields = ("user__username", )
  raw_id_fields = ["user", ]
  
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
  list_display = ("user", "role", "firstName", "lastName")
  list_filter = ("role", )
  search_fields = ("firstName", "lastName")
  raw_id_fields = ["user", ]
  
  actions = ["changeOnStudent","changeOnTeacher"]

  def changeOnStudent(self, request, queryset):
        
        row_update = queryset.update(role='STUDENT')
        if row_update == 1:
            message_bit = "The status of 1 entry has been changed"
        else:
            message_bit = f"The status of {row_update} entries has been changed"
        self.message_user(request, f"{message_bit}")

  def changeOnTeacher(self, request, queryset):
        
        row_update = queryset.update(role='TEACHER')
        if row_update == 1:
            message_bit = "The status of 1 entry has been changed"
        else:
            message_bit = f"The status of {row_update} entries has been changed"
        self.message_user(request, f"{message_bit}")
        
  changeOnStudent.short_description = "Сделать студентом"
  changeOnStudent.allowed_permissions = ('change', )

  changeOnTeacher.short_description = "Сделать учителем"
  changeOnTeacher.allowed_permissions = ('change', )
