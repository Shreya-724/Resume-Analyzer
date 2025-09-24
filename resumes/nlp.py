from .simple_matcher import extract_skills, get_top_recommendations

# Simple wrapper functions
def calculate_similarity(resume_text, job_descriptions):
    from .simple_matcher import get_similarity
    return get_similarity(resume_text, job_descriptions)