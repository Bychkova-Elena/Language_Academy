from django.urls import path
from .views import TeachersCourseView, GetHomeworkView, GetTimeTableView, UpdateDeleteCorseView 

urlpatterns = [
#     path('<int:pk>/timetable/',
#          views.TimeTableView.as_view({'get': 'list'})),
#     path('<int:pk>/homework/',
#          views.HomeworkView.as_view({'get': 'list'})),
    path('courses', TeachersCourseView.as_view()),
    path('courses/<int:courseId>', UpdateDeleteCorseView.as_view()),
    path('<int:pk>/gettimetable', GetTimeTableView.as_view()),
    path('<int:pk>/gethomework', GetHomeworkView.as_view())
]
