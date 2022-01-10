from django.urls import path, include
from .api import RegisterAPI, LoginAPI, UserAPI
from knox import views as knox_views
#from . import views
#from django.contrib.auth import views
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

#urlpatterns = [
    ##path('api/user', views.user, name='user'),
 #   path('login/', views.LoginView.as_view(), name='login'),
  #  path('api/token/obtain', TokenObtainPairView.as_view(), name='token_obtain'),
   # path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
#]

urlpatterns = [
  path('api/auth', include('knox.urls')),
  path('api/auth/register', RegisterAPI.as_view()),
  path('api/auth/login', LoginAPI.as_view()),
  path('api/auth/user', UserAPI.as_view()),
  path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout')
]