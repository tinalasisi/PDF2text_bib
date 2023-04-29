# drive_api.py

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
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

def find_closest_match(drive_service, pattern):
    first_letter = pattern.split('-')[0][0].lower()  # get first letter of "firstauthor"
    subfolder_id = find_subfolder(drive_service, first_letter, FOLDER_ID)
    if subfolder_id is None:
        return None
    file_id = find_subfolder(drive_service, pattern.split('-')[0], subfolder_id)
    return file_id

def find_subfolder(drive_service, folder_name, parent_id):
    results = drive_service.files().list(q=f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and name contains '{folder_name}'", spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    for item in items:
        if item['name'].lower() == folder_name.lower():
            return item['id']
        else:
            return find_subfolder(drive_service, folder_name, item['id'])
    return None
