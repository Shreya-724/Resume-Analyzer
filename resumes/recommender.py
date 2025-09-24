from .models import Job
from .nlp import get_top_recommendations

def recommend_jobs_for_resume(resume_text, top_n=5):
    """Get job recommendations for a resume"""
    jobs = Job.objects.all()
    
    if not jobs:
        return []
    
    # Get top recommendations
    recommendations = get_top_recommendations(resume_text, jobs, top_n)
    
    return recommendations

def recommend_jobs_for_resume_id(resume_id):
    """Get job recommendations for a resume by ID"""
    from .models import Resume
    
    try:
        resume = Resume.objects.get(id=resume_id)
        return recommend_jobs_for_resume(resume.extracted_text)
    except Resume.DoesNotExist:
        return []