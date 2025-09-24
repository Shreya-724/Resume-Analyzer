from .simple_matcher import extract_skills, get_top_recommendations, calculate_similarity_simple

# Compatibility functions
def calculate_similarity(resume_text, job_descriptions):
    """Compatibility function - processes multiple job descriptions"""
    similarities = []
    for job_desc in job_descriptions:
        similarity = calculate_similarity_simple(resume_text, job_desc)
        similarities.append(similarity)
    return similarities