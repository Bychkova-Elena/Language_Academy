from django.urls import path
from .views import GetCourseView, GetHomeworkView, GetTimeTableView, UpdateDeleteCorseView 

urlpatterns = [
    path('courses', GetCourseView.as_view()),
    path('courses/<int:courseId>', UpdateDeleteCorseView.as_view()),
    path('<int:pk>/gettimetable', GetTimeTableView.as_view()),
    path('<int:pk>/gethomework', GetHomeworkView.as_view())
]