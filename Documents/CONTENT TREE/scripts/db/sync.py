#!/usr/bin/env python3
"""
Sync Content/ folder → SQLite database.
Walks all files in Content/, detects metadata, UPSERTs into content_files.

Usage:
    python scripts/db/sync.py            # full sync
    python scripts/db/sync.py --dry-run  # show what would change
"""

import argparse
import hashlib
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from scripts.db.constants import EXCLUDED_DIRS
from scripts.db.shared import (
    count_words,
    detect_content_type,
    detect_language,
    extract_body,
    extract_frontmatter,
    extract_status,
    extract_title,
    parse_content_path,
    should_skip,
)

DB_PATH = os.path.join(PROJECT_ROOT, "content.db")
CONTENT_DIR = os.path.join(PROJECT_ROOT, "Content")

# Google Drive URL mapping (optional)
DRIVE_URL_MAPPING = {}
_drive_map_path = os.path.join(PROJECT_ROOT, "scripts", "drive_url_mapping.json")
if os.path.exists(_drive_map_path):
    import json
    with open(_drive_map_path, "r", encoding="utf-8") as _f:
        DRIVE_URL_MAPPING = json.load(_f)


def file_hash(file_path: str) -> str:
    """MD5 hash of file content for change detection."""
    h = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
    except Exception:
        return ""
    return h.hexdigest()


def scan_content_dir(content_dir: str):
    """Walk Content/ and yield (rel_path, abs_path) for every file."""
    for root, dirs, files in os.walk(content_dir):
        # Filter excluded dirs in-place
        dirs[:] = [d for d in dirs if not should_skip(d)]

        for filename in files:
            if filename.startswith("."):
                continue
            abs_path = os.path.join(root, filename)
            rel_path = os.path.relpath(abs_path, content_dir)
            yield rel_path, abs_path


def build_record(rel_path: str, abs_path: str) -> dict:
    """Build a content_files record from a file."""
    filename = os.path.basename(rel_path)
    stat = os.stat(abs_path)

    # Path-based metadata
    meta = parse_content_path(rel_path)
    ct = detect_content_type(rel_path, filename)
    lang = detect_language(filename)

    # File content metadata (only for text files)
    ext = os.path.splitext(filename)[1].lower()
    text_exts = {".md", ".txt", ".csv", ".docx"}
    frontmatter = {}
    title = None
    word_count = 0
    status = "draft"

    if ext in text_exts:
        frontmatter = extract_frontmatter(abs_path)
        title = extract_title(abs_path, frontmatter)
        status = extract_status(frontmatter, filename)
        if ext == ".md":
            word_count = count_words(abs_path)

    # Drive URL
    drive_url = frontmatter.get("driveUrl") or frontmatter.get("drive_url")
    if not drive_url:
        drive_url = DRIVE_URL_MAPPING.get(rel_path)

    return {
        "path": rel_path,
        "name": filename,
        "product": meta["product"],
        "stage": meta["stage"],
        "category": meta["category"],
        "topic": meta["topic"],
        "content_type": ct,
        "language": lang,
        "status": status,
        "title": title,
        "word_count": word_count,
        "size": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "content_hash": file_hash(abs_path),
        "drive_url": drive_url,
    }


def migrate_fts(cursor):
    """Ensure FTS5 table is standalone (not external-content)."""
    row = cursor.execute(
        "SELECT sql FROM sqlite_master WHERE name='content_fts'"
    ).fetchone()
    if row is None:
        cursor.execute("""CREATE VIRTUAL TABLE content_fts USING fts5(
            file_id UNINDEXED, path, title, body
        )""")
        print("Created content_fts table.")
        return True  # force re-index
    if "content=" in row[0]:
        cursor.execute("DROP TABLE content_fts")
        cursor.execute("""CREATE VIRTUAL TABLE content_fts USING fts5(
            file_id UNINDEXED, path, title, body
        )""")
        print("Migrated content_fts to standalone FTS5.")
        return True
    return False


def upsert_fts(cursor, file_id: int, path: str, title: str, abs_path: str):
    """Insert or replace FTS5 entry for a file."""
    cursor.execute("DELETE FROM content_fts WHERE file_id=?", (str(file_id),))
    body = extract_body(abs_path)
    cursor.execute(
        "INSERT INTO content_fts (file_id, path, title, body) VALUES (?, ?, ?, ?)",
        (str(file_id), path, title or "", body),
    )


def sync(dry_run: bool = False):
    """Main sync: Content/ → SQLite."""
    if not os.path.exists(DB_PATH):
        print(f"Error: database not found at {DB_PATH}")
        print("Run: python scripts/db/init_db.py")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Ensure FTS5 table is correct
    force_reindex = migrate_fts(cursor)

    # Load existing records
    cursor.execute("SELECT path, content_hash FROM content_files")
    existing = {row["path"]: row["content_hash"] for row in cursor.fetchall()}
    if force_reindex:
        existing = {k: None for k in existing}  # force all as "changed"

    added = 0
    updated = 0
    unchanged = 0
    seen_paths = set()

    for rel_path, abs_path in scan_content_dir(CONTENT_DIR):
        seen_paths.add(rel_path)
        record = build_record(rel_path, abs_path)

        # Skip files without a recognized product
        if record["product"] is None:
            continue

        if rel_path not in existing:
            # New file
            if dry_run:
                print(f"  ADD  {rel_path}")
            else:
                cursor.execute(
                    """INSERT INTO content_files
                       (path, name, product, stage, category, topic,
                        content_type, language, status, title, word_count,
                        size, modified, content_hash, drive_url)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        record["path"], record["name"], record["product"],
                        record["stage"], record["category"], record["topic"],
                        record["content_type"], record["language"], record["status"],
                        record["title"], record["word_count"], record["size"],
                        record["modified"], record["content_hash"], record["drive_url"],
                    ),
                )
                file_id = cursor.execute(
                    "SELECT id FROM content_files WHERE path=?", (record["path"],)
                ).fetchone()["id"]
                upsert_fts(cursor, file_id, record["path"], record["title"], abs_path)
            added += 1

        elif existing[rel_path] != record["content_hash"]:
            # Changed file
            if dry_run:
                print(f"  UPD  {rel_path}")
            else:
                cursor.execute(
                    """UPDATE content_files SET
                       name=?, product=?, stage=?, category=?, topic=?,
                       content_type=?, language=?, status=?, title=?, word_count=?,
                       size=?, modified=?, content_hash=?, drive_url=?
                       WHERE path=?""",
                    (
                        record["name"], record["product"], record["stage"],
                        record["category"], record["topic"], record["content_type"],
                        record["language"], record["status"], record["title"],
                        record["word_count"], record["size"], record["modified"],
                        record["content_hash"], record["drive_url"],
                        record["path"],
                    ),
                )
                file_id = cursor.execute(
                    "SELECT id FROM content_files WHERE path=?", (record["path"],)
                ).fetchone()["id"]
                upsert_fts(cursor, file_id, record["path"], record["title"], abs_path)
            updated += 1

        else:
            # Backfill FTS if missing
            if not dry_run:
                file_row = cursor.execute(
                    "SELECT id FROM content_files WHERE path=?", (rel_path,)
                ).fetchone()
                if file_row:
                    fts_exists = cursor.execute(
                        "SELECT 1 FROM content_fts WHERE file_id=?", (str(file_row["id"]),)
                    ).fetchone()
                    if not fts_exists:
                        upsert_fts(cursor, file_row["id"], rel_path, record["title"], abs_path)
            unchanged += 1

    # Deleted files (in DB but not on disk)
    deleted_paths = set(existing.keys()) - seen_paths
    deleted = 0
    for path in deleted_paths:
        if dry_run:
            print(f"  DEL  {path}")
        else:
            row = cursor.execute(
                "SELECT id FROM content_files WHERE path=?", (path,)
            ).fetchone()
            if row:
                cursor.execute("DELETE FROM content_fts WHERE file_id=?", (str(row["id"]),))
            cursor.execute("DELETE FROM content_files WHERE path=?", (path,))
        deleted += 1

    if not dry_run:
        conn.commit()

    # Summary
    cursor.execute("SELECT COUNT(*) FROM content_files")
    total = cursor.fetchone()[0]
    fts_count = cursor.execute("SELECT COUNT(*) FROM content_fts").fetchone()[0]
    conn.close()

    prefix = "[DRY RUN] " if dry_run else ""
    print(f"\n{prefix}Sync complete:")
    print(f"  Added:     {added}")
    print(f"  Updated:   {updated}")
    print(f"  Deleted:   {deleted}")
    print(f"  Unchanged: {unchanged}")
    print(f"  Total in DB: {total}")
    print(f"  FTS indexed: {fts_count}")


def main():
    parser = argparse.ArgumentParser(description="Sync Content/ → SQLite")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without applying")
    args = parser.parse_args()
    sync(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
