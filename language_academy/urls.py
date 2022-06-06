from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include("users.urls")),
    path('api/v1/', include("education.urls")),
    path('api/v1/', include("languages.urls")),
    path('api/v1/', include("permissions.urls")),
    path('api/v1/', include("core.urls")),
    path('api_schema/', get_schema_view(
        title='API Schema',
        description='Guide for the REST API'
    ), name='api_schema'),
    path('docs/', TemplateView.as_view(
        template_name='docs.html',
        extra_context={'schema_url':'api_schema'}
        ), name='swagger-ui'),
    path('api-auth/', include("rest_framework.urls")),
    path('djoser/', include('djoser.urls')),
    path('djoser/', include('djoser.urls.jwt')),
    path('', include('frontend.urls')),
]
