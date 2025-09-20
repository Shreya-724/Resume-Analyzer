import spacy
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from django.conf import settings

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model 'en_core_web_sm'...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Load skills list
def load_skills_list():
    """Load skills from CSV file"""
    skills_path = os.path.join(settings.BASE_DIR, 'skills.csv')
    try:
        skills_df = pd.read_csv(skills_path)
        return set(skills_df['skill'].str.lower().tolist())
    except FileNotFoundError:
        # Return a default set of skills if file not found
        return {
            'python', 'javascript', 'java', 'c++', 'html', 'css', 'sql', 
            'django', 'flask', 'react', 'angular', 'vue', 'node.js',
            'machine learning', 'data analysis', 'project management',
            'communication', 'problem solving', 'teamwork', 'leadership'
        }

SKILLS_LIST = load_skills_list()

def extract_skills(text):
    """Extract skills from text using both pattern matching and NLP"""
    text = text.lower()
    found_skills = set()
    
    # Method 1: Direct matching with skills list
    for skill in SKILLS_LIST:
        if skill in text:
            found_skills.add(skill)
    
    # Method 2: NLP-based extraction using noun chunks and entities
    doc = nlp(text)
    
    # Extract noun phrases that might represent skills
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.lower().strip()
        if chunk_text in SKILLS_LIST:
            found_skills.add(chunk_text)
    
    # Extract entities that might be skills
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "SKILL"]:
            ent_text = ent.text.lower().strip()
            if ent_text in SKILLS_LIST:
                found_skills.add(ent_text)
    
    return list(found_skills)

def create_tfidf_vectorizer(job_descriptions):
    """Create and fit a TF-IDF vectorizer on job descriptions"""
    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_features=5000,
        ngram_range=(1, 2)  # Include both single words and bigrams
    )
    vectorizer.fit(job_descriptions)
    return vectorizer

def calculate_similarity(resume_text, job_descriptions, vectorizer=None):
    """Calculate similarity between resume and job descriptions"""
    if not vectorizer:
        vectorizer = create_tfidf_vectorizer(job_descriptions)
    
    # Transform both resume and job descriptions
    all_texts = [resume_text] + job_descriptions
    tfidf_matrix = vectorizer.transform(all_texts)
    
    # Calculate cosine similarity between resume and each job
    resume_vector = tfidf_matrix[0:1]
    job_vectors = tfidf_matrix[1:]
    
    similarities = cosine_similarity(resume_vector, job_vectors)
    return similarities[0]

def get_top_recommendations(resume_text, jobs, top_n=5):
    """Get top job recommendations based on similarity"""
    job_descriptions = [job.description for job in jobs]
    
    # Calculate similarities
    similarities = calculate_similarity(resume_text, job_descriptions)
    
    # Pair jobs with their similarity scores
    job_scores = list(zip(jobs, similarities))
    
    # Sort by similarity (descending)
    job_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return top N recommendations
    return job_scores[:top_n]