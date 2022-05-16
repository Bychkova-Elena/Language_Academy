from django.urls import path
from .views import (CoursesView, CourseView, GetHomeworkView, GetTimeTableView,
                    UpdateDeleteHomeworkView, AddHomeworkView)

urlpatterns = [
    path('courses', CoursesView.as_view()),
    path('courses/<int:courseId>', CourseView.as_view()),
    path('courses/<int:courseId>/homeworks', GetHomeworkView.as_view()),
    path('courses/<int:courseId>/homeworks/add', AddHomeworkView.as_view()),
    path('homeworks/<int:homeworkId>', UpdateDeleteHomeworkView.as_view()),
    path('<int:pk>/gettimetable', GetTimeTableView.as_view()),
]
