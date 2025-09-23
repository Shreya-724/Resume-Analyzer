from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import generics, permissions
from .models import Resume, Job,UserProfile
from .forms import ResumeUploadForm,UserProfileForm, UserForm
from .serializers import ResumeSerializer, JobSerializer
from .parsers import parse_resume
from .nlp import extract_skills
from .recommender import recommend_jobs_for_resume_id
from django.contrib import messages


def home(request):
    """Home page view"""
    if request.user.is_authenticated:
        return redirect('resume_list')
    return render(request, 'resumes/home.html')

def signup_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('resume_list')
    else:
        form = UserCreationForm()
    return render(request, 'resumes/signup.html', {'form': form})

def login_view(request):
    """User login view"""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('resume_list')
    else:
        form = AuthenticationForm()
    return render(request, 'resumes/login.html', {'form': form})

def logout_view(request):
    """User logout view"""
    logout(request)
    return redirect('home')

@login_required
def resume_list(request):
    """List all resumes for the current user"""
    resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_at')
    
    # Pagination
    paginator = Paginator(resumes, 10)  # Show 10 resumes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'resumes/resume_list.html', {'page_obj': page_obj})

@login_required
def resume_upload(request):
    """Handle resume upload"""
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.original_filename = request.FILES['file'].name
            
            # Parse resume and extract text
            try:
                resume.extracted_text = parse_resume(
                    request.FILES['file'], 
                    request.FILES['file'].name
                )
                
                # Extract skills from text
                resume.skills = extract_skills(resume.extracted_text)
                
                resume.save()
                return redirect('resume_list')
            except Exception as e:
                form.add_error('file', f"Error processing file: {str(e)}")
    else:
        form = ResumeUploadForm()
    
    return render(request, 'resumes/resume_upload.html', {'form': form})

@login_required
def resume_detail(request, pk):
    """Show resume details and recommendations"""
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    recommendations = recommend_jobs_for_resume_id(pk)
    
    return render(request, 'resumes/resume_detail.html', {
        'resume': resume,
        'recommendations': recommendations
    })

@login_required
def resume_delete(request, pk):
    """Delete a resume"""
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    
    if request.method == 'POST':
        resume_name = resume.original_filename
        resume.delete()
        messages.success(request, f'Resume "{resume_name}" has been deleted successfully.')
        return redirect('resume_list')
    
    # If not POST, redirect to resume list
    return redirect('resume_list')

@login_required
def profile_view(request):
    """User profile page"""
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
    
    return render(request, 'resumes/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile
    })

@login_required
def profile_picture_upload(request):
    """Handle profile picture upload via AJAX"""
    if request.method == 'POST' and request.FILES:
        try:
            profile = request.user.userprofile
            profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            return JsonResponse({'success': True, 'profile_picture_url': profile.get_profile_picture_url})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
# API Views
class ResumeListAPI(generics.ListCreateAPIView):
    """API view to list and create resumes"""
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Handle file upload and processing
        file = self.request.FILES['file']
        extracted_text = parse_resume(file, file.name)
        skills = extract_skills(extracted_text)
        
        serializer.save(
            user=self.request.user,
            original_filename=file.name,
            extracted_text=extracted_text,
            skills=skills
        )

class ResumeDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, or delete a resume"""
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

class ResumeRecommendationsAPI(View):
    """API view to get job recommendations for a resume"""
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        recommendations = recommend_jobs_for_resume_id(pk)
        
        # Format recommendations for JSON response
        rec_data = []
        for job, score in recommendations:
            rec_data.append({
                'job_id': job.id,
                'title': job.title,
                'company': job.company,
                'similarity_score': round(float(score), 3),
                'description': job.description[:200] + '...' if len(job.description) > 200 else job.description
            })
        
        return JsonResponse({
            'resume_id': resume.id,
            'resume_name': resume.original_filename,
            'recommendations': rec_data
        })