# API URLs (separate file)
from django.urls import path
from . import views

api_urlpatterns = [
    path('resumes/', views.ResumeListAPI.as_view(), name='api_resume_list'),
    path('resumes/<int:pk>/', views.ResumeDetailAPI.as_view(), name='api_resume_detail'),
    path('resumes/<int:pk>/recommendations/', views.ResumeRecommendationsAPI.as_view(), name='api_resume_recommendations'),
]