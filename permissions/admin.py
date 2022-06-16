from django.contrib import admin

from .models import Permission


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "key",
        "targetUserId",
        "targetUserIdKey",
        "targetCourseId",
        "targetCourseIdKey"
    )
