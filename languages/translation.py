from modeltranslation.translator import register, TranslationOptions
from .models import Language, Level

@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(Level)
class LevelTranslationOptions(TranslationOptions):
    fields = ('name', )
