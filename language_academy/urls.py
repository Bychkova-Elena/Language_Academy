
from django.contrib import admin
from django.urls import path
from django.urls.conf import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include("education.urls")),
    path('api/v1/', include("languages.urls")),
    path('api/v1/', include("users.urls")),
    path('api/v1/auth/', include("core.urls")),
    path('api-auth/', include("rest_framework.urls")),
    path('djoser/', include('djoser.urls')),
    path('djoser/', include('djoser.urls.jwt')),
    path('', include('frontend.urls')),
]


