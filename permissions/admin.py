from django.contrib import admin

from .models import Permission


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "permissionKey",
        "targetUserId",
        "targetUserIdKey",
        "targetCourseId",
        "targetCourseIdKey"
    )
