from rest_framework import serializers
from .models import Resume, Job

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'original_filename', 'uploaded_at', 'skills']
        read_only_fields = ['id', 'original_filename', 'uploaded_at', 'skills']

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'company', 'description', 'required_skills', 'location', 'posted_date']