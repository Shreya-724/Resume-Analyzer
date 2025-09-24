import re
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings

def load_skills_list():
    """Load skills from CSV file"""
    skills_path = os.path.join(settings.BASE_DIR, 'skills.csv')
    try:
        skills_df = pd.read_csv(skills_path)
        return set(skills_df['skill'].str.lower().tolist())
    except FileNotFoundError:
        return {
            'python', 'javascript', 'java', 'html', 'css', 'sql', 
            'django', 'flask', 'react', 'node.js', 'machine learning',
            'data analysis', 'project management', 'communication'
        }

def extract_skills(text):
    """Simple skill extraction without spaCy"""
    text = text.lower()
    skills_list = load_skills_list()
    found_skills = []
    
    # Simple keyword matching
    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found_skills.append(skill)
    
    return found_skills

def get_similarity(resume_text, job_descriptions):
    """Simple TF-IDF similarity"""
    if not job_descriptions:
        return []
    
    vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
    all_texts = [resume_text] + job_descriptions
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    resume_vector = tfidf_matrix[0:1]
    job_vectors = tfidf_matrix[1:]
    
    similarities = cosine_similarity(resume_vector, job_vectors)
    return similarities[0]

def get_top_recommendations(resume_text, jobs, top_n=5):
    """Get top job recommendations"""
    job_descriptions = [job.description for job in jobs]
    
    if not job_descriptions:
        return []
    
    similarities = get_similarity(resume_text, job_descriptions)
    job_scores = list(zip(jobs, similarities))
    job_scores.sort(key=lambda x: x[1], reverse=True)
    
    return job_scores[:top_n]