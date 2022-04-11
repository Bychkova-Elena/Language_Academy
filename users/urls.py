from django.urls import path

<<<<<<< HEAD
from .views import UserProfileDetailView, UserProfileListCreateView
=======
from .views import UserProfileListCreateView, userProfileDetailView, LanguageTeachersView
>>>>>>> Group: updating and deleting teachers groups

urlpatterns = [
    # gets all user profiles and create a new profile
    path("all-profiles", UserProfileListCreateView.as_view(), name="all-profiles"),
    # retrieves profile details of the currently logged in user
<<<<<<< HEAD
    path("profile/<int:pk>", UserProfileDetailView.as_view(), name="profile"),
=======
    path("profile/<int:pk>", userProfileDetailView.as_view(), name="profile"),
    path("languages", LanguageTeachersView.as_view()),
>>>>>>> Group: updating and deleting teachers groups
]
