from django.urls import path
from .views import (CoursesView, CourseView, HomeworksView, GetTimeTableView,
                    HomeworkView, AllHomeworksView)

urlpatterns = [
    path('courses', CoursesView.as_view()),
    path('homeworks', AllHomeworksView.as_view()),
    path('courses/<int:courseId>', CourseView.as_view()),
    path('courses/<int:courseId>/homeworks', HomeworksView.as_view()),
    path('courses/<int:courseId>/homeworks/<int:homeworkId>', HomeworkView.as_view()),
    path('courses/<int:courseId>/timetable', GetTimeTableView.as_view()),

]
