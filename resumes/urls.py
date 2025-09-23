from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('resumes/', views.resume_list, name='resume_list'),
    path('resumes/upload/', views.resume_upload, name='resume_upload'),
    path('resumes/<int:pk>/', views.resume_detail, name='resume_detail'),
    path('resumes/<int:pk>/delete/', views.resume_delete, name='resume_delete'),
    path('profile/', views.profile_view, name='profile'),
]