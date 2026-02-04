#!/usr/bin/env python3
"""
Initialize Content Tree SQLite database.
Creates content.db, applies schema, populates reference tables.

Usage:
    python scripts/db/init_db.py          # create/reset DB
    python scripts/db/init_db.py --force  # drop and recreate all tables
"""

import argparse
import os
import sqlite3
import sys

# Ensure project root is importable
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from scripts.db.constants import (
    CONTENT_TYPES,
    LANGUAGES,
    PRIORITY_RULES,
    TOPICS,
    display_name,
)

DB_PATH = os.path.join(PROJECT_ROOT, "content.db")
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")


def create_database(force: bool = False) -> str:
    """Create content.db and populate reference tables. Returns DB path."""
    if force and os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed existing {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Apply schema
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    print("Schema applied.")

    # Populate topics
    topic_count = 0
    for category, topic_list in TOPICS.items():
        for topic_name in topic_list:
            cursor.execute(
                "INSERT OR IGNORE INTO topics (category, name, display_name) VALUES (?, ?, ?)",
                (category, topic_name, display_name(topic_name)),
            )
            topic_count += cursor.rowcount
    print(f"Topics: {topic_count} inserted.")

    # Populate content_types
    ct_count = 0
    for name, disp in CONTENT_TYPES:
        cursor.execute(
            "INSERT OR IGNORE INTO content_types (name, display_name) VALUES (?, ?)",
            (name, disp),
        )
        ct_count += cursor.rowcount
    print(f"Content types: {ct_count} inserted.")

    # Populate languages
    lang_count = 0
    for code, name, is_primary in LANGUAGES:
        cursor.execute(
            "INSERT OR IGNORE INTO languages (code, name, is_primary) VALUES (?, ?, ?)",
            (code, name, int(is_primary)),
        )
        lang_count += cursor.rowcount
    print(f"Languages: {lang_count} inserted.")

    # Populate priorities
    pri_count = 0
    for stage, category, content_type, language, priority, label in PRIORITY_RULES:
        cursor.execute(
            "INSERT OR IGNORE INTO priorities (stage, category, content_type, language, priority, priority_label) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (stage, category, content_type, language, priority, label),
        )
        pri_count += cursor.rowcount
    print(f"Priority rules: {pri_count} inserted.")

    conn.commit()

    # Summary
    cursor.execute("SELECT COUNT(*) FROM topics")
    total_topics = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM content_types")
    total_ct = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM languages")
    total_lang = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM priorities")
    total_pri = cursor.fetchone()[0]

    print(f"\n--- Database ready: {DB_PATH} ---")
    print(f"  Topics:         {total_topics}")
    print(f"  Content types:  {total_ct}")
    print(f"  Languages:      {total_lang}")
    print(f"  Priority rules: {total_pri}")

    conn.close()
    return DB_PATH


def main():
    parser = argparse.ArgumentParser(description="Initialize Content Tree database")
    parser.add_argument("--force", action="store_true", help="Drop and recreate DB")
    args = parser.parse_args()

    db_path = create_database(force=args.force)
    print(f"\nDone. DB at: {db_path}")


if __name__ == "__main__":
    main()
