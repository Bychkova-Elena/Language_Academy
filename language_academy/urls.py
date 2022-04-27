
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('education/', include("education.urls")),
    path('users/', include("users.urls")),
    path('api/v1/', include("core.urls")),
    path('api/v1/', include("permissions.urls")),
    path('api-auth/', include("rest_framework.urls")),
    path('djoser/', include('djoser.urls')),
    path('djoser/', include('djoser.urls.jwt')),
    path('', include('frontend.urls')),
]
