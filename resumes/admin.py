from django.contrib import admin
from .models import Resume, Job

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