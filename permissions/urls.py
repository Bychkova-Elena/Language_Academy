from django.urls import path

from .views import PermissionsView

urlpatterns = [
    path('permissions', PermissionsView.as_view()),
]
