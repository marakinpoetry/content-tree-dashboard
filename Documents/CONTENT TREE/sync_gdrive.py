#!/usr/bin/env python3
"""
Sync Content folder from Google Drive and create ID mapping for clickable links
"""
import os
import io
import json
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CONTENT_FOLDER_NAME = 'Content'
MAPPING_FILE = 'gdrive_ids.json'

# Set to True if using Shared Drive (corporate Google Workspace)
USE_SHARED_DRIVE = True

# Will store: { "Content/Pre-Registration/file.md": {"id": "xxx", "type": "file"} }
drive_mapping = {}


def get_service():
    """Create Google Drive API service using service account credentials"""
    creds = service_account.Credentials.from_service_account_file(
        'credentials.json', scopes=SCOPES
    )
    return build('drive', 'v3', credentials=creds)


def find_folder(service, name, parent_id=None):
    """Find a folder by name in Google Drive (supports Shared Drives)"""
    query = f"name='{name}' and mimeType='application/vnd.google-apps.folder'"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    # Parameters for Shared Drive support
    params = {
        'q': query,
        'fields': 'files(id, name)',
        'supportsAllDrives': USE_SHARED_DRIVE,
        'includeItemsFromAllDrives': USE_SHARED_DRIVE
    }

    results = service.files().list(**params).execute()
    files = results.get('files', [])
    return files[0] if files else None


def download_folder(service, folder_id, local_path, relative_path=""):
    """Recursively download folder contents and track Google Drive IDs"""
    global drive_mapping

    local_path = Path(local_path)
    local_path.mkdir(parents=True, exist_ok=True)

    # Store folder ID
    if relative_path:
        drive_mapping[relative_path] = {
            "id": folder_id,
            "type": "folder",
            "url": f"https://drive.google.com/drive/folders/{folder_id}"
        }

    # Get all items in folder (supports Shared Drives)
    query = f"'{folder_id}' in parents and trashed=false"
    page_token = None

    while True:
        results = service.files().list(
            q=query,
            fields="nextPageToken, files(id, name, mimeType)",
            pageSize=1000,
            pageToken=page_token,
            supportsAllDrives=USE_SHARED_DRIVE,
            includeItemsFromAllDrives=USE_SHARED_DRIVE
        ).execute()

        for item in results.get('files', []):
            item_path = local_path / item['name']
            item_relative = f"{relative_path}/{item['name']}" if relative_path else item['name']

            if item['mimeType'] == 'application/vnd.google-apps.folder':
                # Recursively download subfolders
                download_folder(service, item['id'], item_path, item_relative)
            else:
                # Store file ID
                drive_mapping[item_relative] = {
                    "id": item['id'],
                    "type": "file",
                    "url": f"https://drive.google.com/file/d/{item['id']}/view"
                }

                # Download file (supports Shared Drives)
                try:
                    request = service.files().get_media(
                        fileId=item['id'],
                        supportsAllDrives=USE_SHARED_DRIVE
                    )
                    with open(item_path, 'wb') as f:
                        downloader = MediaIoBaseDownload(f, request)
                        done = False
                        while not done:
                            _, done = downloader.next_chunk()
                    print(f"  {item_relative}")
                except Exception as e:
                    print(f"  {item_relative}: {e}")

        page_token = results.get('nextPageToken')
        if not page_token:
            break


def main():
    global drive_mapping
    drive_mapping = {}

    print("Connecting to Google Drive...")
    service = get_service()

    # Find the Content folder shared with service account
    folder = find_folder(service, CONTENT_FOLDER_NAME)
    if not folder:
        print(f"ERROR: Folder '{CONTENT_FOLDER_NAME}' not found!")
        print("Make sure the folder is shared with the service account email.")
        return

    print(f"Found folder: {CONTENT_FOLDER_NAME} (ID: {folder['id']})")

    # Store root folder mapping
    drive_mapping["Content"] = {
        "id": folder['id'],
        "type": "folder",
        "url": f"https://drive.google.com/drive/folders/{folder['id']}"
    }

    # Download Content folder
    print(f"\nSyncing {CONTENT_FOLDER_NAME} folder...")
    download_folder(service, folder['id'], './Content', 'Content')

    # Save mapping file for dashboard
    with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(drive_mapping, f, indent=2, ensure_ascii=False)

    print(f"\nSync complete!")
    print(f"  Files/folders mapped: {len(drive_mapping)}")
    print(f"  Mapping saved to: {MAPPING_FILE}")


if __name__ == '__main__':
    main()
