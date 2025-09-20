import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from resumes.models import Job

class Command(BaseCommand):
    help = 'Load sample jobs from JSON file'
    
    def handle(self, *args, **options):
        # Path to sample jobs file
        file_path = os.path.join(settings.BASE_DIR, 'sample_jobs.json')
        
        try:
            with open(file_path, 'r') as file:
                jobs_data = json.load(file)
                
            # Delete existing jobs
            Job.objects.all().delete()
            
            # Create new jobs
            for job_data in jobs_data:
                Job.objects.create(
                    title=job_data['title'],
                    company=job_data['company'],
                    description=job_data['description'],
                    required_skills=job_data.get('required_skills', []),
                    location=job_data.get('location', '')
                )
                
            self.stdout.write(
                self.style.SUCCESS(f'Successfully loaded {len(jobs_data)} jobs')
            )
            
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR('Sample jobs file not found. Please make sure sample_jobs.json exists in the project root.')
            )