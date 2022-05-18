from django.contrib import admin

from .models import Students, Teachers, UserProfile, UserRole


@admin.register(Teachers)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("user",)
    list_filter = ("language", )
    search_fields = ("user__username", )
    raw_id_fields = ["user", ]

@admin.register(Students)
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

    actions = ["ChangeOnStudent","ChangeOnTeacher"]

    def ChangeOnStudent(self, request, queryset):
        rowUpdate = queryset.update(role=UserRole.STUDENT)

        if rowUpdate == 1:
            messageBit = "The status of 1 entry has been changed"
        else:
            messageBit = f"The status of {rowUpdate} entries has been changed"

        self.message_user(request, f"{messageBit}")

    def ChangeOnTeacher(self, request, queryset):
        rowUpdate = queryset.update(role=UserRole.TEACHER)

        if rowUpdate == 1:
            messageBit = "The status of 1 entry has been changed"
        else:
            messageBit = f"The status of {rowUpdate} entries has been changed"

        self.message_user(request, f"{messageBit}")

    ChangeOnStudent.short_description = "Сделать студентом"
    ChangeOnStudent.allowed_permissions = ('change', )

    ChangeOnTeacher.short_description = "Сделать учителем"
    ChangeOnTeacher.allowed_permissions = ('change', )
