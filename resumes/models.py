import os
import uuid
import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

def resume_file_path(instance, filename):
    """Generate file path for resume"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('resumes', filename)

def user_profile_picture_path(instance, filename):
    """Generate file path for profile pictures"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('profile_pictures', filename)

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

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to=user_profile_picture_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def get_profile_picture_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            try:
                return self.profile_picture.url
            except:
                # Fallback to Gravatar if file upload fails
                return self.get_gravatar_url()
        return self.get_gravatar_url()
    
    def get_gravatar_url(self, size=150):
        """Get Gravatar URL for user email"""
        email = self.user.email.lower().encode('utf-8')
        email_hash = hashlib.md5(email).hexdigest()
        return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon"
    
    def save(self, *args, **kwargs):
        """Handle file saving for Render compatibility"""
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            # If file save fails, continue without profile picture
            self.profile_picture = None
            super().save(*args, **kwargs)