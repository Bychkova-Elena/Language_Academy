
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.urls.conf import include, re_path
from django.views.generic import TemplateView

# def index_view(request):
#     return render(request, 'build/index.html')

urlpatterns = [
    path('admin', admin.site.urls),
    path('education/', include("education.urls")),
    path('users/', include("users.urls")),
    path('core/', include("core.urls")),
    path('api-auth/', include("rest_framework.urls")),
    path('', include('frontend.urls')),
]

# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
