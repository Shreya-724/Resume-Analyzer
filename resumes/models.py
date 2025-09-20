import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

def resume_file_path(instance, filename):
    """Generate file path for resume"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('resumes', filename)

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=resume_file_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'txt'])]
    )
    original_filename = models.CharField(max_length=255)
    extracted_text = models.TextField(blank=True)
    skills = models.JSONField(default=list, blank=True)  # Store extracted skills
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.original_filename}"

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    required_skills = models.JSONField(default=list, blank=True)
    location = models.CharField(max_length=255, blank=True)
    posted_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} at {self.company}"