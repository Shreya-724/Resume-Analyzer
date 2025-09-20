from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from .models import Resume, Job
from .parsers import parse_resume, clean_text
from .nlp import extract_skills
from .recommender import recommend_jobs_for_resume

class ParserTests(TestCase):
    def test_clean_text(self):
        """Test text cleaning function"""
        dirty_text = "  Hello   World!\nThis is a test.  "
        cleaned = clean_text(dirty_text)
        self.assertEqual(cleaned, "Hello World! This is a test.")
        
    def test_text_extraction(self):
        """Test text extraction from different file types"""
        # Test TXT file
        txt_file = SimpleUploadedFile("test.txt", b"This is a test resume content. Skills: Python, JavaScript.")
        text = parse_resume(txt_file, "test.txt")
        self.assertIn("test resume content", text)
        
class NLPTests(TestCase):
    def test_skill_extraction(self):
        """Test skill extraction from text"""
        text = "I have experience with Python, JavaScript, and Django. Also familiar with React and Node.js."
        skills = extract_skills(text)
        
        # Should extract at least these skills
        expected_skills = {'python', 'javascript', 'django', 'react', 'node.js'}
        self.assertTrue(expected_skills.issubset(set(skills)))
        
class RecommenderTests(TestCase):
    def setUp(self):
        # Create test jobs
        self.job1 = Job.objects.create(
            title="Python Developer",
            company="Test Company",
            description="We need a Python developer with Django experience",
            required_skills=["Python", "Django"]
        )
        
        self.job2 = Job.objects.create(
            title="Frontend Developer",
            company="Test Company",
            description="Looking for a JavaScript and React developer",
            required_skills=["JavaScript", "React"]
        )
        
    def test_recommendation(self):
        """Test job recommendation based on resume text"""
        resume_text = "I am a Python developer with extensive Django experience and some JavaScript knowledge."
        
        recommendations = recommend_jobs_for_resume(resume_text, top_n=2)
        
        # Should recommend at least one job
        self.assertGreater(len(recommendations), 0)
        
        # Python job should have higher similarity than frontend job
        python_job_score = None
        frontend_job_score = None
        
        for job, score in recommendations:
            if job.title == "Python Developer":
                python_job_score = score
            elif job.title == "Frontend Developer":
                frontend_job_score = score
                
        self.assertIsNotNone(python_job_score)
        self.assertIsNotNone(frontend_job_score)
        self.assertGreater(python_job_score, frontend_job_score)
        
class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass123'
        )
        
    def test_resume_creation(self):
        """Test creating a resume"""
        resume = Resume.objects.create(
            user=self.user,
            original_filename="test.pdf",
            extracted_text="Test resume content",
            skills=["Python", "JavaScript"]
        )
        
        self.assertEqual(resume.user.username, 'testuser')
        self.assertEqual(resume.original_filename, 'test.pdf')
        self.assertIn('Python', resume.skills)