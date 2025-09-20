"""
URL configuration for resume_analyzer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from resumes import views as resume_views

# API URLs
api_urlpatterns = [
    path('resumes/', resume_views.ResumeListAPI.as_view(), name='api_resume_list'),
    path('resumes/<int:pk>/', resume_views.ResumeDetailAPI.as_view(), name='api_resume_detail'),
    path('resumes/<int:pk>/recommendations/', resume_views.ResumeRecommendationsAPI.as_view(), name='api_resume_recommendations'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('resumes.urls')),
    path('api/', include(api_urlpatterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)