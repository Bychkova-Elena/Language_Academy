from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('timetable/<int:pk>/',
         views.TimeTableView.as_view({'get': 'list'})),
]