from django.urls import path

from .views import CoursesView, CourseView, GetHomeworkView, GetTimeTableView

urlpatterns = [
    path('courses', CoursesView.as_view()),
    path('courses/<int:courseId>', CourseView.as_view()),
    path('<int:pk>/gettimetable', GetTimeTableView.as_view()),
    path('<int:pk>/gethomework', GetHomeworkView.as_view())
]
