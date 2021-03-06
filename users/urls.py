from django.urls import path
from .views import (UserProfileListCreateView, UserProfileDetailView,
                    StudentsView)
urlpatterns = [
    # gets all user profiles and create a new profile
    path("all-profiles", UserProfileListCreateView.as_view(), name="all-profiles"),
    # retrieves profile details of the currently logged in user
    path("profile/<int:pk>", UserProfileDetailView.as_view(), name="profile"),
    path('courses/<int:courseId>/students', StudentsView.as_view()),
]
