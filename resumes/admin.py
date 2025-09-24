from django.contrib import admin
from .models import Resume, Job, UserProfile

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['user', 'original_filename', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['user__username', 'original_filename']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'posted_date']
    list_filter = ['posted_date', 'company']
    search_fields = ['title', 'company', 'description']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'location']
    search_fields = ['user__username', 'phone_number', 'location']