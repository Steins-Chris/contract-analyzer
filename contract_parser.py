
import PyPDF2
from docx import Document
import re

def extract_text_from_file(file_path):
    try:
        if file_path.endswith('.pdf'):
            return extract_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            return extract_from_docx(file_path)
        elif file_path.endswith('.txt'):
            return extract_from_txt(file_path)
        else:
            return None
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def extract_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return clean_text(text)

def extract_from_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return clean_text(text)

def extract_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return clean_text(text)

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,;:()\-]', '', text)
    return text.strip()

