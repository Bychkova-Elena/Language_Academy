from django.urls import path

from .views import LevelView, LanguageTeachersView

urlpatterns = [
    path("levels", LevelView.as_view()),
    path("languages", LanguageTeachersView.as_view()),

]
