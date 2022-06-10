from django.contrib import admin

from modeltranslation.admin import TabbedTranslationAdmin
from .models import Language, Level


@admin.register(Language)
class LanguageAdmin(TabbedTranslationAdmin):
    list_display = ("name", )
    search_fields = ("name", )

@admin.register(Level)
class LevelAdmin(TabbedTranslationAdmin):
    list_display = ("name", )
    search_fields = ("name", )
