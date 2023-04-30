# main.py

import os
import glob
import sys
import re

from drive_api import load_gdrive_creds, download_pdf, find_closest_match
from pdf_processing import pdf_to_text
from folder_checker import check_folder
from bibtex_processing import process_bibtex, generate_pattern


# def clean_author_names(author_string):
#     authors = author_string.split(' and ')
#     last_names = [name.split(', ')[0] for name in authors]
#     return ', '.join(last_names)

def clean_author_names(author_string):
    authors = author_string.split(' and ')
    last_names = [name.split(', ')[0] for name in authors]
    if len(authors) == 1:
        return last_names[0]
    elif len(authors) == 2:
        return f"{last_names[0]} and {last_names[1]}"
    else:
        return f"{last_names[0]} et al."


def remove_bibtex_formats(title):
    return title.replace('{', '').replace('}', '')


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

# # Generate a list of filenames from the .bib file and save the entries
# print("Generating filenames from .bib file...")
# filenames, entries = process_bibtex(bib_files[0])
# entries_dict = {filename + '.pdf': entry for filename, entry in zip(filenames, entries)}
# print("Done generating filenames.")

# # Initialize the Google Drive service
# print("Initializing Google Drive service...")
# drive_service = load_gdrive_creds()
# print("Done initializing Google Drive service.")

# # Download PDFs for each filename and save them in the 'pdf' folder
# print("Downloading PDFs...")
# for filename in filenames:
#     file_id = find_closest_match(drive_service, filename)
#     if file_id:
#         download_pdf(drive_service, file_id, os.path.join(pdf_folder_path, filename + '.pdf'))
# print("Done downloading PDFs.")

# Generate a list of filenames from the .bib file and save the entries
print("Generating filenames from .bib file...")
filenames, entries = process_bibtex(bib_files[0])
entries_dict = {filename + '.pdf': entry for filename, entry in zip(filenames, entries)}
print("Done generating filenames.")

# Initialize the Google Drive service
print("Initializing Google Drive service...")
drive_service = load_gdrive_creds()
print("Done initializing Google Drive service.")

# Download PDFs for each filename and save them in the 'pdf' folder
print("Downloading PDFs...")
for filename in filenames:
    full_file_path = os.path.join(pdf_folder_path, filename + '.pdf')
    if not os.path.isfile(full_file_path):  # Check if file already exists
        file_id = find_closest_match(drive_service, filename)
        if file_id:
            download_pdf(drive_service, file_id, full_file_path)
        else:
            print(f"No match found for {filename}. Skipping this file.")
    else:
        print(f"File {filename} already exists. Skipping download.")
print("Done downloading PDFs.")


# # Convert each PDF to a txt file and save it in the 'txt' folder
# print("Converting PDFs to txt files...")
# pdf_files = glob.glob(os.path.join(pdf_folder_path, "*.pdf"))
# for pdf_file in pdf_files:
#     txt_filename = os.path.splitext(os.path.basename(pdf_file))[0] + '.txt'
#     txt_filepath = os.path.join(txt_folder_path, txt_filename)
    
#     # Extract entry data
#     entry = entries_dict.get(os.path.basename(pdf_file))
#     if entry is None:
#         print(f"No entry found for {os.path.basename(pdf_file)}. Skipping this file.")
#         continue

#     authors = clean_author_names(entry['author'])
#     journal = entry['journal']
#     year = entry['year']
#     title = remove_bibtex_formats(entry['title'])

#     # preamble = f"This is an article by {authors} published in {journal} in {year} entitled {title}. \n \n"
#     preamble = f"This is an article by {authors} published in {journal} in {year} entitled {title}"
#     preamble = re.sub('\s+', ' ', preamble) + '\n\n'

    
#     pdf_to_text(pdf_file, txt_filepath, preamble)

#     # Rename txt files based on the journal and year
#     txt_files = glob.glob(os.path.join(txt_folder_path, "*.txt"))
#     for txt_file in txt_files:
#         old_name = os.path.basename(txt_file)
#         filename, ext = os.path.splitext(old_name)
#         year = re.findall(r"\d{4}", filename)[-1]
#         journal = entry['journal']
#         # Replace illegal characters with underscores
#         journal_short = re.search('\((.*?)\)', journal)
#         if journal_short is not None:
#             journal_short = journal_short.group(1).replace(':', '').replace('/', '_').rstrip().replace(' ', '_')
#         else:
#             journal_short = journal.replace(':', '').replace('/', '_').rstrip().replace(' ', '_')
#         new_name = f"{filename.rsplit('_', maxsplit=1)[0]}_{journal_short}{ext}"
#         os.rename(txt_file, os.path.join(txt_folder_path, new_name))
    
    
# print("Done converting PDFs to txt files.")

# Convert each PDF to a txt file and save it in the 'txt' folder
print("Converting PDFs to txt files...")
pdf_files = glob.glob(os.path.join(pdf_folder_path, "*.pdf"))
for pdf_file in pdf_files:
    # Extract entry data
    entry = entries_dict.get(os.path.basename(pdf_file))
    if entry is None:
        print(f"No entry found for {os.path.basename(pdf_file)}. Skipping this file.")
        continue

    authors = clean_author_names(entry['author'])
    journal = entry.get('journal', 'Unknown Journal')  # Update this line
    year = entry['year']
    title = remove_bibtex_formats(entry['title'])

    preamble = f"This is an article by {authors} published in {journal} in {year} entitled {title}"
    preamble = re.sub('\s+', ' ', preamble) + '\n\n'
    
    # Generate filename based on your logic in bibtex_processing.py
    txt_filename = generate_pattern(entry, mode=2) + '.txt'
    txt_filepath = os.path.join(txt_folder_path, txt_filename)
    
    pdf_to_text(pdf_file, txt_filepath, preamble)

print("Done converting PDFs to txt files.")



