# pdf_processing.py

from PyPDF2 import PdfReader

def pdf_to_text(pdf_path, txt_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        text = ''.join(page.extract_text() for page in reader.pages)
        
    with open(txt_path, 'w') as txt_file:
        txt_file.write(text)
