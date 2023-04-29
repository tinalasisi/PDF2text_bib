# pdf_processing.py

from PyPDF2 import PdfFileReader

def pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PdfFileReader(pdf_file)
        text = reader.extract_text()
    return text
