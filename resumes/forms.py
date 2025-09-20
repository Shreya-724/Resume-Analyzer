from django import forms
from .models import Resume

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (max 5MB)
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File too large. Max size is 5MB.")
            
            # Get file extension
            ext = file.name.split('.')[-1].lower()
            if ext not in ['pdf', 'docx', 'txt']:
                raise forms.ValidationError("Invalid file type. Only PDF, DOCX, and TXT files are allowed.")
                
        return file