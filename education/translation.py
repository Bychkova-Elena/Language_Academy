from modeltranslation.translator import register, TranslationOptions
from .models import Course, Homework

@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(Homework)
class HomeworkTranslationOptions(TranslationOptions):
    fields = ('name', 'description' )
