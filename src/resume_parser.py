import PyPDF2 
import re

def extract_text_from_pdf(file): 
    reader = PyPDF2.PdfReader(file) 
    text = "" 
    for page in reader.pages:
         text += page.extract_text() or ""
    return text.lower()

def extract_text_from_txt(file): 
    return file.read().decode("utf-8").lower()

def clean_text(text):
     text = re.sub(r"[^a-zA-Z0-9 ]", " ", text) 
     text = re.sub(r"\s+", " ", text) 
     return text.strip().lower()
