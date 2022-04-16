from django.urls import path
from .views import SignupView, LoginView,  LogoutView, DeleteAccountView, GetUsersView, TokenRefreshView, MeView

from rest_framework_simplejwt.views import (
    TokenVerifyView
)

urlpatterns = [
    path('delete', DeleteAccountView.as_view()),
    path('getusers', GetUsersView.as_view()),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),

    path('register', SignupView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('me', MeView.as_view()),
]
