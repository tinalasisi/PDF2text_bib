# main.py

import os
import glob
import sys

from drive_api import load_gdrive_creds, download_pdf, find_closest_match
from pdf_processing import pdf_to_text
from folder_checker import check_folder
from bibtex_processing import process_bibtex

workspace_path = os.path.join(os.getcwd(), 'workspace')
bibtex_folder_path = os.path.join(workspace_path, 'bibtex')
pdf_folder_path = os.path.join(workspace_path, 'pdf')
txt_folder_path = os.path.join(workspace_path, 'txt')

# Check and create folders if they don't exist
print("Checking and creating necessary folders...")
check_folder(workspace_path)
check_folder(bibtex_folder_path)
check_folder(pdf_folder_path)
check_folder(txt_folder_path)
print("Done checking and creating folders.")

# Look for a .bib file in the 'bibtex' folder
print("Looking for .bib file...")
bib_files = glob.glob(os.path.join(bibtex_folder_path, "*.bib"))

if not bib_files:
    print("No .bib file found in the 'bibtex' folder. Please add a .bib file and run the script again.")
    sys.exit(1)

print("Found .bib file.")

# Generate a list of filenames from the .bib file
print("Generating filenames from .bib file...")
process_bibtex(bib_files[0])
print("Done generating filenames.")

# Load filenames from 'filenames.txt' file
with open(os.path.join(bibtex_folder_path, 'filenames.txt'), 'r') as f:
    filenames = [line.strip() for line in f]

# Initialize the Google Drive service
print("Initializing Google Drive service...")
drive_service = load_gdrive_creds()
print("Done initializing Google Drive service.")

# Download PDFs for each filename and save them in the 'pdf' folder
print("Downloading PDFs...")
for filename in filenames:
    file_id = find_closest_match(drive_service, filename)
    if file_id:
        download_pdf(drive_service, file_id, os.path.join(pdf_folder_path, filename))
print("Done downloading PDFs.")

# Convert each PDF to a txt file and save it in the 'txt' folder
print("Converting PDFs to txt files...")
pdf_files = glob.glob(os.path.join(pdf_folder_path, "*.pdf"))
for pdf_file in pdf_files:
    txt_filename = os.path.splitext(os.path.basename(pdf_file))[0] + '.txt'
    txt_filepath = os.path.join(txt_folder_path, txt_filename)
    pdf_to_text(pdf_file, txt_filepath)
print("Done converting PDFs to txt files.")
