from django.urls import path
from .views import SignupView, LoginView,  LogoutView, DeleteAccountView, GetUsersView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('register', SignupView.as_view()),
    path('logout', LogoutView.as_view()),
    path('delete', DeleteAccountView.as_view()),
    path('getusers', GetUsersView.as_view()),

    path('login', LoginView.as_view()),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
]
