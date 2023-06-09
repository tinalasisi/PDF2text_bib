# bibtex_processing.py

import os
import glob
import bibtexparser

# def generate_pattern(entry, mode=1):
#     journal = entry.get('journal', '')  # Use an empty string if 'journal' doesn't exist
#     year = entry['year']
#     title = entry['title'].replace(' ', '-').replace('{', '').replace('}', '').replace('\n', '')

#     authors = entry['author'].split(' and ')
#     for i in range(len(authors)):
#         if ',' in authors[i]:  # if author is in format "LastName, FirstName"
#             authors[i] = authors[i].split(',')[0]  # take only the last name

#     if len(authors) > 2:
#         authors = authors[0] + "-et-al"
#     elif len(authors) == 2:
#         authors = '-and-'.join(authors)
#     else:  # There is only one author
#         authors = authors[0]

#     if mode == 1:
#         return f"{authors}_{year}_{title}"
#     else:  # mode 2
#         return f"{authors}_{journal}_{year}_{title}"

import string

def generate_pattern(entry, mode=1):
    journal = entry.get('journal', '')  # Use an empty string if 'journal' doesn't exist
    year = entry['year']
    title = entry['title'].replace(' ', '-').replace('{', '').replace('}', '').replace('\n', '')

    authors = entry['author'].split(' and ')
    for i in range(len(authors)):
        if ',' in authors[i]:  # if author is in format "LastName, FirstName"
            authors[i] = authors[i].split(',')[0]  # take only the last name

    if len(authors) > 2:
        authors = authors[0] + "-et-al"
    elif len(authors) == 2:
        authors = '-and-'.join(authors)
    else:  # There is only one author
        authors = authors[0]

    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

    if mode == 1:
        pattern = f"{authors}_{year}_{title}"
    else:  # mode 2
        pattern = f"{authors}_{journal}_{year}_{title}"

    # Remove invalid characters
    pattern = ''.join(c for c in pattern if c in valid_chars)

    # Limit the length of the pattern to prevent OSError: [Errno 63] File name too long
    max_length = 250  # Maximum filename length for most filesystems
    if len(pattern) > max_length:
        pattern = pattern[:max_length]

    return pattern





def process_bibtex(bibtex_file, mode=1):
    if not os.path.exists(bibtex_file):
        raise FileNotFoundError(f"No bibtex file found at {bibtex_file}")

    with open(bibtex_file) as bibtex_data:
        bib_database = bibtexparser.load(bibtex_data)

    filenames = []
    entries = []
    for entry in bib_database.entries:
        pattern = generate_pattern(entry, mode)
        filename = pattern.replace(' ', '-')
        filenames.append(filename + '.pdf')  # Add .pdf extension
        entries.append(entry)

    # Write filenames to a txt file in the 'bibtex' folder
    if not os.path.exists('workspace/bibtex'):
        os.makedirs('workspace/bibtex')

    with open(os.path.join('workspace/bibtex', 'filenames.txt'), 'w') as f:
        for filename in filenames:
            f.write(f"{filename}\n")
        
        return filenames, entries

