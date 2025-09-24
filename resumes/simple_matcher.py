import re
import os
import csv
from django.conf import settings

def load_skills_list():
    """Load skills from CSV file without pandas or scikit-learn"""
    skills_path = os.path.join(settings.BASE_DIR, 'skills.csv')
    skills_set = set()
    
    try:
        with open(skills_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'skill' in row:
                    skills_set.add(row['skill'].lower())
    except FileNotFoundError:
        # Return basic skills if file not found
        skills_set = {
            'python', 'javascript', 'java', 'html', 'css', 'sql', 
            'django', 'flask', 'react', 'node.js', 'machine learning',
            'data analysis', 'project management', 'communication',
            'c++', 'aws', 'docker', 'git', 'linux', 'mysql', 'postgresql',
            'api', 'rest', 'agile', 'scrum', 'teamwork', 'problem solving'
        }
    
    return skills_set

def extract_skills(text):
    """Simple skill extraction"""
    text = text.lower()
    skills_list = load_skills_list()
    found_skills = []
    
    # Simple keyword matching
    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found_skills.append(skill)
    
    return found_skills

def calculate_similarity_simple(resume_text, job_description):
    """Ultra-simple similarity using word overlap (Jaccard similarity)"""
    if not resume_text or not job_description:
        return 0.0
    
    # Convert to sets of words
    resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
    job_words = set(re.findall(r'\b\w+\b', job_description.lower()))
    
    # Calculate Jaccard similarity
    if not resume_words or not job_words:
        return 0.0
    
    intersection = resume_words.intersection(job_words)
    union = resume_words.union(job_words)
    
    return len(intersection) / len(union)

def get_top_recommendations(resume_text, jobs, top_n=5):
    """Get top job recommendations using simple word overlap"""
    if not jobs:
        return []
    
    # Calculate similarities using simple word overlap
    job_scores = []
    for job in jobs:
        similarity = calculate_similarity_simple(resume_text, job.description)
        job_scores.append((job, similarity))
    
    # Sort by similarity (descending)
    job_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return top N recommendations
    return job_scores[:top_n]