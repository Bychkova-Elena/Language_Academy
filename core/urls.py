from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from .views import (DeleteAccountView, GetUsersView, LoginView, LogoutView,
                    MeView, SignupView, TokenRefreshView)

urlpatterns = [
    path('auth/delete', DeleteAccountView.as_view()),
    path('auth/getusers', GetUsersView.as_view()),
    path('auth/token/verify', TokenVerifyView.as_view(), name='token_verify'),

    path('auth/register', SignupView.as_view()),
    path('auth/login', LoginView.as_view()),
    path('auth/logout', LogoutView.as_view()),
    path('auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('me', MeView.as_view()),
]
