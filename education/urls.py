from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('<int:pk>/timetable/',
         views.TimeTableView.as_view({'get': 'list'})),
    path('<int:pk>/homework/',
         views.HomeworkView.as_view({'get': 'list'})),
]