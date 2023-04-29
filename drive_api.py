# drive_api.py

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials  # Update this line
from difflib import get_close_matches
import io

from config import FOLDER_ID, SCOPES


def load_gdrive_creds():
    creds = Credentials.from_service_account_file('gdrive_creds.json', scopes=SCOPES)
    print("Google Drive credentials loaded")
    return build('drive', 'v3', credentials=creds)

def download_pdf(drive_service, file_id, filename):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))


def find_file(drive_service, filename):
    # Query files with filename wildcard
    results = drive_service.files().list(
        q=f"name contains '{filename}' and mimeType='application/pdf'", 
        spaces='drive', 
        fields='files(id, name)'
    ).execute()

    items = results.get('files', [])
    if items:  # If any items are found
        return items[0]['id']  # Return ID of first match
    return None


def find_closest_match(drive_service, pattern):
    pattern_parts = pattern.split('-')
    
    for i in range(len(pattern_parts), 0, -1):
        partial_pattern = '-'.join(pattern_parts[:i])
        file_id = find_file(drive_service, partial_pattern)
        if file_id is not None:
            return file_id
        else:
            print(f"No file found for {partial_pattern}")
    return None



