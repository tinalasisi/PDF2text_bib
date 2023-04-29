# main.py

import os
import glob
import sys
import bibtexparser

from drive_api import load_gdrive_creds, download_pdf, find_closest_match
from pdf_processing import pdf_to_text
from folder_checker import check_folder

def get_filenames_from_bibtex(bib_filepath):
    with open(bib_filepath, 'r') as bibfile:
        bib_database = bibtexparser.load(bibfile)
    return [f"{entry['author'].split(',')[0]}-et-al_{entry['year']}_{entry['title']}.pdf" for entry in bib_database.entries]

workspace_path = os.path.join(os.getcwd(), 'workspace')
bibtex_folder_path = os.path.join(workspace_path, 'bibtex')
pdf_folder_path = os.path.join(workspace_path, 'pdf')
txt_folder_path = os.path.join(workspace_path, 'txt')

# Check and create folders if they don't exist
check_folder(workspace_path)
check_folder(bibtex_folder_path)
check_folder(pdf_folder_path)
check_folder(txt_folder_path)

# Look for a .bib file in the 'bibtex' folder
bib_files = glob.glob(os.path.join(bibtex_folder_path, "*.bib"))

if not bib_files:
    print("No .bib file found in the 'bibtex' folder. Please add a .bib file and run the script again.")
    sys.exit(1)

# Generate a list of filenames from the .bib file
filenames = get_filenames_from_bibtex(bib_files[0])

# Initialize the Google Drive service
drive_service = load_gdrive_creds()

# Download PDFs for each filename and save them in the 'pdf' folder
for filename in filenames:
    file_id = find_closest_match(drive_service, filename)
    if file_id:
        download_pdf(drive_service, file_id, os.path.join(pdf_folder_path, filename))

# Convert each PDF to a txt file and save it in the 'txt' folder
pdf_files = glob.glob(os.path.join(pdf_folder_path, "*.pdf"))
for pdf_file in pdf_files:
    txt_filename = os.path.splitext(os.path.basename(pdf_file))[0] + '.txt'
    txt_filepath = os.path.join(txt_folder_path, txt_filename)
    pdf_to_text(pdf_file, txt_filepath)
