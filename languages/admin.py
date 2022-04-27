from django.contrib import admin

from .models import Language, Level


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", )
    search_fields = ("name", )

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("name", )
    search_fields = ("name", )
