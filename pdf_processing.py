# pdf_processing.py

from PyPDF2 import PdfReader

def pdf_to_text(pdf_path, txt_path, preamble=""):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        text = ''.join(page.extract_text() for page in reader.pages)

    # Write text to file
    with open(txt_path, 'w') as f:
        f.write(preamble)
        f.write(text)
