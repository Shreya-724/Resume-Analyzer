import re
from io import StringIO
from pdfminer.high_level import extract_text as extract_pdf_text
from pdfminer.layout import LAParams
from docx import Document

def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    try:
        # Create a string buffer to capture the text
        output_string = StringIO()
        
        # Extract text with layout parameters for better text extraction
        laparams = LAParams()
        text = extract_pdf_text(file, laparams=laparams)
        
        return clean_text(text)
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    try:
        doc = Document(file)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        return clean_text(text)
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")

def extract_text_from_txt(file):
    """Extract text from TXT file"""
    try:
        text = file.read().decode('utf-8')
        return clean_text(text)
    except Exception as e:
        raise Exception(f"Error extracting text from TXT: {str(e)}")

def clean_text(text):
    """Clean and normalize extracted text"""
    if not text:
        return ""
    
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    
    # Remove non-printable characters but keep common punctuation
    text = re.sub(r'[^\x20-\x7E\u00A0-\u024F]', ' ', text)
    
    # Normalize spaces
    text = ' '.join(text.split())
    
    return text.strip()

def parse_resume(file, filename):
    """Parse resume file based on extension and return text"""
    ext = filename.split('.')[-1].lower()
    
    if ext == 'pdf':
        return extract_text_from_pdf(file)
    elif ext == 'docx':
        return extract_text_from_docx(file)
    elif ext == 'txt':
        return extract_text_from_txt(file)
    else:
        raise ValueError("Unsupported file format")