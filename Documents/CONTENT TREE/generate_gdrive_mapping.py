#!/usr/bin/env python3
"""
Generate Google Drive ID mapping from rclone
Maps local file paths to Google Drive URLs for dashboard clickable links
"""

import subprocess
import json
from pathlib import Path

# Configuration
RCLONE_REMOTE = "wscontentdrive"
DRIVE_PATH = "Content"
OUTPUT_FILE = Path(__file__).parent / "gdrive_ids.json"

def get_drive_url(file_id: str, is_dir: bool) -> str:
    """Convert Google Drive ID to URL"""
    if is_dir:
        return f"https://drive.google.com/drive/folders/{file_id}"
    else:
        return f"https://drive.google.com/file/d/{file_id}/view"

def main():
    print(f"🔍 Fetching file list from {RCLONE_REMOTE}:{DRIVE_PATH}...")

    # Run rclone lsjson to get file IDs
    result = subprocess.run(
        ["rclone", "lsjson", f"{RCLONE_REMOTE}:{DRIVE_PATH}", "--recursive"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"❌ Error running rclone: {result.stderr}")
        return

    # Parse JSON output
    files = json.loads(result.stdout)
    print(f"   Found {len(files)} items")

    # Build mapping
    mapping = {}
    for item in files:
        path = f"Content/{item['Path']}"
        file_id = item.get('ID')
        is_dir = item.get('IsDir', False)

        if file_id:
            mapping[path] = {
                'id': file_id,
                'url': get_drive_url(file_id, is_dir),
                'isDir': is_dir,
                'name': item.get('Name', ''),
                'mimeType': item.get('MimeType', '')
            }

    # Save mapping
    print(f"\n💾 Saving mapping to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    # Print summary
    dirs = sum(1 for v in mapping.values() if v['isDir'])
    files_count = len(mapping) - dirs
    print(f"\n✅ Generated mapping for {len(mapping)} items:")
    print(f"   📁 Folders: {dirs}")
    print(f"   📄 Files: {files_count}")
    print(f"\n🔗 Example URLs:")

    # Show a few examples
    count = 0
    for path, info in mapping.items():
        if count >= 3:
            break
        if not info['isDir'] and path.endswith('.md'):
            print(f"   {path}")
            print(f"   → {info['url']}")
            count += 1

if __name__ == '__main__':
    main()
