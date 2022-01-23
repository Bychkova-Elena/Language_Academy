from django.urls import path, include
from .api import RegistrationAPI, LoginAPI, UserAPI
# from knox import views as knox_views
from . import views
#from django.contrib.auth import views
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

#urlpatterns = [
    ##path('api/user', views.user, name='user'),
 #   path('login/', views.LoginView.as_view(), name='login'),
  #  path('api/token/obtain', TokenObtainPairView.as_view(), name='token_obtain'),
   # path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
#]

# urlpatterns = [
  # path('api/auth', include('knox.urls')),
  # path('api/auth/register', RegistrationAPI.as_view()),
  # path('api/auth/login', LoginAPI.as_view()),
  # path('api/auth/user', UserAPI.as_view()),
  # path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
#   path('login/', views.login_view, name='api-login'),
#   path('logout/', views.logout_view, name='api-logout'),
#   path('session/', views.session_view, name='api-session'),
#   path('whoami/', views.whoami_view, name='api-whoami'),
  
# ]

from .views import SignupView, GetCSRFToken, LoginView, LogoutView, CheckAuthenticatedView, DeleteAccountView, GetUsersView

urlpatterns = [
    path('authenticated', CheckAuthenticatedView.as_view()),
    path('register', SignupView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('delete', DeleteAccountView.as_view()),
    path('csrf_cookie', GetCSRFToken.as_view()),
    path('get_users', GetUsersView.as_view())
]