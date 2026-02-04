#!/usr/bin/env python3
"""
Export SQLite → data.json for Dashboard.
Generates coverage matrix, gaps, stats from content_files table.

Usage:
    python scripts/db/export.py
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

DB_PATH = os.path.join(PROJECT_ROOT, "content.db")
DASHBOARD_JSON = os.path.join(PROJECT_ROOT, "Dashboard", "data.json")
REPO_ROOT_JSON = os.path.join(os.path.expanduser("~"), "data.json")


def get_connection():
    if not os.path.exists(DB_PATH):
        print(f"Error: database not found at {DB_PATH}")
        print("Run: python scripts/db/init_db.py && python scripts/db/sync.py")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def export_files(conn) -> list:
    """Export all content_files as list of dicts."""
    cursor = conn.execute(
        """SELECT id, path, name, product, stage, category, topic,
                  content_type, language, status, title, word_count,
                  size, modified, drive_url
           FROM content_files
           ORDER BY modified DESC"""
    )
    files = []
    for row in cursor:
        files.append({
            "id": row["id"],
            "path": row["path"],
            "name": row["name"],
            "product": row["product"],
            "stage": row["stage"],
            "category": row["category"],
            "topic": row["topic"],
            "content_type": row["content_type"],
            "language": row["language"],
            "status": row["status"],
            "title": row["title"],
            "word_count": row["word_count"],
            "size": row["size"],
            "modified": row["modified"],
            "drive_url": row["drive_url"],
        })
    return files


def export_coverage(conn) -> dict:
    """
    Build coverage matrix: category → language → topic → {content_type: count}.
    Only for files with category and topic (WS 1.0 / WS 2.0 hierarchical).
    """
    cursor = conn.execute(
        """SELECT category, language, topic, content_type, COUNT(*) as cnt
           FROM content_files
           WHERE category IS NOT NULL AND category != ''
             AND topic IS NOT NULL AND topic != ''
           GROUP BY category, language, topic, content_type"""
    )

    coverage = {}
    for row in cursor:
        cat = row["category"]
        lang = row["language"] or "unknown"
        topic = row["topic"]
        ct = row["content_type"]

        coverage.setdefault(cat, {})
        coverage[cat].setdefault(lang, {})
        coverage[cat][lang].setdefault(topic, {})
        coverage[cat][lang][topic][ct] = row["cnt"]

    return coverage


def export_gaps(conn) -> list:
    """
    Find gaps: topic × content_type × language combinations that have 0 files.
    Uses priorities table for severity labeling.
    """
    # Get all topics, content types, languages
    topics = conn.execute("SELECT name, display_name, category FROM topics").fetchall()
    content_types = conn.execute(
        "SELECT name FROM content_types WHERE name NOT IN ('other', 'static_ad', 'video_ad')"
    ).fetchall()
    languages = conn.execute("SELECT code FROM languages WHERE is_primary = 1").fetchall()

    # Get existing combinations
    existing = set()
    cursor = conn.execute(
        """SELECT topic, content_type, language
           FROM content_files
           WHERE topic IS NOT NULL AND topic != ''
             AND content_type IS NOT NULL
             AND language IS NOT NULL AND language != ''"""
    )
    for row in cursor:
        existing.add((row["topic"], row["content_type"], row["language"]))

    # Load priority rules
    priority_rules = conn.execute(
        "SELECT stage, category, content_type, language, priority, priority_label FROM priorities"
    ).fetchall()

    gaps = []
    for topic_row in topics:
        topic_name = topic_row["name"]
        topic_display = topic_row["display_name"]
        topic_category = topic_row["category"]

        for ct_row in content_types:
            ct_name = ct_row["name"]

            for lang_row in languages:
                lang_code = lang_row["code"]

                if (topic_name, ct_name, lang_code) not in existing:
                    # Find matching priority rule (most specific first)
                    priority = 4
                    priority_label = "Low"

                    for rule in priority_rules:
                        r_stage = rule["stage"]
                        r_cat = rule["category"]
                        r_ct = rule["content_type"]
                        r_lang = rule["language"]

                        ct_match = r_ct is None or r_ct == ct_name
                        lang_match = r_lang is None or r_lang == lang_code
                        cat_match = r_cat is None or r_cat == topic_category

                        if ct_match and lang_match and cat_match:
                            if rule["priority"] < priority:
                                priority = rule["priority"]
                                priority_label = rule["priority_label"]

                    gaps.append({
                        "topic": topic_name,
                        "topic_display": topic_display,
                        "category": topic_category,
                        "content_type": ct_name,
                        "language": lang_code,
                        "priority": priority,
                        "priority_label": priority_label,
                    })

    # Sort: critical first, then by category/topic
    gaps.sort(key=lambda g: (g["priority"], g["category"], g["topic"]))
    return gaps


def export_stats(conn) -> dict:
    """Aggregate stats by language, category, content_type, status."""
    stats = {}

    # By language
    by_language = {}
    cursor = conn.execute(
        """SELECT language, status, COUNT(*) as cnt
           FROM content_files
           WHERE language IS NOT NULL AND language != ''
           GROUP BY language, status"""
    )
    for row in cursor:
        lang = row["language"]
        by_language.setdefault(lang, {"total": 0, "published": 0, "draft": 0, "idea": 0})
        by_language[lang][row["status"]] = by_language[lang].get(row["status"], 0) + row["cnt"]
        by_language[lang]["total"] += row["cnt"]
    stats["by_language"] = by_language

    # By category
    by_category = {}
    cursor = conn.execute(
        """SELECT category, COUNT(*) as cnt
           FROM content_files
           WHERE category IS NOT NULL AND category != ''
           GROUP BY category"""
    )
    for row in cursor:
        by_category[row["category"]] = row["cnt"]
    stats["by_category"] = by_category

    # By content_type
    by_content_type = {}
    cursor = conn.execute(
        "SELECT content_type, COUNT(*) as cnt FROM content_files GROUP BY content_type"
    )
    for row in cursor:
        by_content_type[row["content_type"]] = row["cnt"]
    stats["by_content_type"] = by_content_type

    # By status
    by_status = {}
    cursor = conn.execute(
        "SELECT status, COUNT(*) as cnt FROM content_files GROUP BY status"
    )
    for row in cursor:
        by_status[row["status"]] = row["cnt"]
    stats["by_status"] = by_status

    # By product
    by_product = {}
    cursor = conn.execute(
        "SELECT product, COUNT(*) as cnt FROM content_files GROUP BY product"
    )
    for row in cursor:
        by_product[row["product"]] = row["cnt"]
    stats["by_product"] = by_product

    # By stage
    by_stage = {}
    cursor = conn.execute(
        """SELECT product, stage, COUNT(*) as cnt
           FROM content_files
           GROUP BY product, stage"""
    )
    for row in cursor:
        label = row["stage"] or row["product"]
        key = f"{row['product']}/{row['stage']}" if row["stage"] else row["product"]
        by_stage[key] = row["cnt"]
    stats["by_stage"] = by_stage

    return stats


def export_topics(conn) -> list:
    """Export topics reference."""
    cursor = conn.execute("SELECT name, display_name, category FROM topics ORDER BY category, name")
    return [dict(row) for row in cursor]


def export_content_types(conn) -> list:
    """Export content_types reference."""
    cursor = conn.execute("SELECT name, display_name FROM content_types ORDER BY id")
    return [dict(row) for row in cursor]


def export_languages(conn) -> list:
    """Export languages reference."""
    cursor = conn.execute("SELECT code, name, is_primary FROM languages ORDER BY is_primary DESC, code")
    return [{"code": row["code"], "name": row["name"], "is_primary": bool(row["is_primary"])} for row in cursor]


def export():
    """Main export: SQLite → data.json."""
    conn = get_connection()

    total = conn.execute("SELECT COUNT(*) FROM content_files").fetchone()[0]

    data = {
        "generated_at": datetime.now().isoformat(),
        "total_files": total,
        "files": export_files(conn),
        "coverage": export_coverage(conn),
        "gaps": export_gaps(conn),
        "stats": export_stats(conn),
        "topics": export_topics(conn),
        "content_types": export_content_types(conn),
        "languages": export_languages(conn),
    }

    conn.close()

    # Save to Dashboard/data.json
    os.makedirs(os.path.dirname(DASHBOARD_JSON), exist_ok=True)
    with open(DASHBOARD_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    size_kb = os.path.getsize(DASHBOARD_JSON) / 1024
    print(f"Saved: {DASHBOARD_JSON} ({size_kb:.0f} KB)")

    # Save to repo root (GitHub Pages)
    try:
        with open(REPO_ROOT_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved: {REPO_ROOT_JSON}")
    except Exception as e:
        print(f"Warning: could not save to {REPO_ROOT_JSON}: {e}")

    # Summary
    print(f"\nExport complete:")
    print(f"  Total files:    {data['total_files']}")
    print(f"  Coverage cells: {sum(len(topics) for lang_data in data['coverage'].values() for topics in lang_data.values())}")
    print(f"  Gaps found:     {len(data['gaps'])}")
    print(f"  Topics:         {len(data['topics'])}")
    gap_crit = sum(1 for g in data["gaps"] if g["priority"] == 1)
    gap_high = sum(1 for g in data["gaps"] if g["priority"] == 2)
    gap_med = sum(1 for g in data["gaps"] if g["priority"] == 3)
    gap_low = sum(1 for g in data["gaps"] if g["priority"] == 4)
    print(f"  Gaps by priority: Critical={gap_crit}, High={gap_high}, Medium={gap_med}, Low={gap_low}")


if __name__ == "__main__":
    export()
