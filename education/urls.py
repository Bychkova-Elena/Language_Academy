from django.urls import path
from .views import (GetCourseView, GetHomeworkView, GetTimeTableView, UpdateDeleteCorseView,
                    UpdateDeleteHomeworkView, AddHomeworkView)

urlpatterns = [
    path('courses', GetCourseView.as_view()),
    path('courses/<int:courseId>', UpdateDeleteCorseView.as_view()),
    path('courses/<int:courseId>/homeworks', GetHomeworkView.as_view()),
    path('courses/<int:courseId>/homeworks/add', AddHomeworkView.as_view()),
    path('homeworks/<int:homeworkId>', UpdateDeleteHomeworkView.as_view()),
    path('<int:pk>/gettimetable', GetTimeTableView.as_view()),
]
