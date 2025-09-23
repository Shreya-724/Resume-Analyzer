import re
from io import StringIO,BytesIO
from pdfminer.high_level import extract_text as extract_pdf_text
from pdfminer.layout import LAParams
from docx import Document

def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    try:
        # Reset file pointer to beginning
        if hasattr(file, 'seek'):
            file.seek(0)
        
        # Create a bytes buffer from the uploaded file
        pdf_bytes = file.read()
        
        # Create a bytes buffer for pdfminer
        pdf_buffer = BytesIO(pdf_bytes)
        
        # Extract text with layout parameters for better text extraction
        laparams = LAParams()
        text = extract_pdf_text(pdf_buffer, laparams=laparams)
        
        # Reset file pointer for potential future use
        if hasattr(file, 'seek'):
            file.seek(0)
            
        return clean_text(text)
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    try:
        # Reset file pointer to beginning
        if hasattr(file, 'seek'):
            file.seek(0)
            
        # Create a bytes buffer from the uploaded file
        docx_bytes = file.read()
        
        # Create a bytes buffer for python-docx
        docx_buffer = BytesIO(docx_bytes)
        
        doc = Document(docx_buffer)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        
        # Reset file pointer for potential future use
        if hasattr(file, 'seek'):
            file.seek(0)
            
        return clean_text(text)
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")

def extract_text_from_txt(file):
    """Extract text from TXT file"""
    try:
        # Reset file pointer to beginning
        if hasattr(file, 'seek'):
            file.seek(0)
            
        # Read the file content with proper encoding handling
        try:
            text = file.read().decode('utf-8')
        except UnicodeDecodeError:
            # Try other common encodings if UTF-8 fails
            file.seek(0)
            try:
                text = file.read().decode('latin-1')
            except:
                file.seek(0)
                text = file.read().decode('utf-8', errors='ignore')
        
        # Reset file pointer for potential future use
        if hasattr(file, 'seek'):
            file.seek(0)
            
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
    
    # Reset file pointer to beginning before processing
    if hasattr(file, 'seek'):
        file.seek(0)
    
    if ext == 'pdf':
        return extract_text_from_pdf(file)
    elif ext == 'docx':
        return extract_text_from_docx(file)
    elif ext == 'txt':
        return extract_text_from_txt(file)
    else:
        raise ValueError("Unsupported file format. Please upload PDF, DOCX, or TXT files.")
