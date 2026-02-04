#!/usr/bin/env python3
"""
Search Content Tree database.

Usage:
    python scripts/db/search.py gantt                          # free-text search
    python scripts/db/search.py --product "WS 1.0" --type article
    python scripts/db/search.py kanban --lang ua --status published
    python scripts/db/search.py --category Features --count
    python scripts/db/search.py gantt --json
"""

import argparse
import json
import os
import sqlite3
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

DB_PATH = os.path.join(PROJECT_ROOT, "content.db")

COLUMNS = [
    ("Name",     "name",         30, "left"),
    ("Product",  "product",       8, "left"),
    ("Stage",    "stage",        10, "left"),
    ("Category", "category",     12, "left"),
    ("Topic",    "topic",        16, "left"),
    ("Type",     "content_type",  8, "left"),
    ("Lang",     "language",      4, "left"),
    ("Status",   "status",        9, "left"),
    ("Words",    "word_count",    6, "right"),
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Search Content Tree files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s gantt                              # search for "gantt"
  %(prog)s --product "WS 1.0" --type article  # filter only
  %(prog)s kanban --lang ua --status published # search + filter
  %(prog)s --category Features --count         # count matches
  %(prog)s gantt --json                        # JSON output""",
    )
    parser.add_argument("query", nargs="?", default=None,
                        help="Free-text search query (path, title, body)")
    parser.add_argument("--product", help="Filter: WS 1.0, WS 2.0, WS 2.0 Release")
    parser.add_argument("--stage", help="Filter: Pre-Registration, Trial, Success_Client")
    parser.add_argument("--category", help="Filter: Features, Pains, Competitors, ...")
    parser.add_argument("--topic", help="Filter: Gantt_Chart, Kanban, ...")
    parser.add_argument("--type", dest="content_type", help="Filter: article, landing, video, smm, ...")
    parser.add_argument("--lang", help="Filter: ua, en, ru, pl, ...")
    parser.add_argument("--status", help="Filter: published, draft, idea, ...")
    parser.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")
    parser.add_argument("--json", dest="json_output", action="store_true", help="JSON output")
    parser.add_argument("--count", action="store_true", help="Show only count")
    return parser.parse_args()


def truncate(text, width):
    if text is None:
        return "-"
    text = str(text)
    return text[:width - 1] + "\u2026" if len(text) > width else text


def format_table(rows):
    lines = []
    header = "  ".join(
        h.ljust(w) if a == "left" else h.rjust(w)
        for h, _, w, a in COLUMNS
    )
    lines.append(header)
    lines.append("-" * len(header))
    for row in rows:
        parts = []
        for _, key, width, align in COLUMNS:
            val = truncate(row.get(key), width)
            parts.append(val.rjust(width) if align == "right" else val.ljust(width))
        lines.append("  ".join(parts))
    return "\n".join(lines)


def build_fts_query(args):
    sql = """
        SELECT cf.name, cf.product, cf.stage, cf.category, cf.topic,
               cf.content_type, cf.language, cf.status, cf.word_count,
               cf.path, cf.title, rank
        FROM content_fts fts
        JOIN content_files cf ON cf.id = CAST(fts.file_id AS INTEGER)
        WHERE content_fts MATCH ?
    """
    params = [args.query]
    for col, val in get_filters(args):
        sql += f" AND cf.{col} = ?"
        params.append(val)
    sql += " ORDER BY rank LIMIT ?"
    params.append(args.limit)
    return sql, params


def build_filter_query(args):
    sql = """
        SELECT name, product, stage, category, topic,
               content_type, language, status, word_count,
               path, title, NULL as rank
        FROM content_files
        WHERE 1=1
    """
    params = []
    for col, val in get_filters(args):
        sql += f" AND {col} = ?"
        params.append(val)
    sql += " ORDER BY modified DESC LIMIT ?"
    params.append(args.limit)
    return sql, params


def build_like_query(args):
    like = f"%{args.query}%"
    sql = """
        SELECT name, product, stage, category, topic,
               content_type, language, status, word_count,
               path, title, NULL as rank
        FROM content_files
        WHERE (path LIKE ? OR title LIKE ? OR name LIKE ?)
    """
    params = [like, like, like]
    for col, val in get_filters(args):
        sql += f" AND {col} = ?"
        params.append(val)
    sql += " ORDER BY modified DESC LIMIT ?"
    params.append(args.limit)
    return sql, params


def get_filters(args):
    mapping = [
        ("product", args.product),
        ("stage", args.stage),
        ("category", args.category),
        ("topic", args.topic),
        ("content_type", args.content_type),
        ("language", args.lang),
        ("status", args.status),
    ]
    return [(col, val) for col, val in mapping if val is not None]


def main():
    args = parse_args()

    if not os.path.exists(DB_PATH):
        print(f"Error: database not found at {DB_PATH}", file=sys.stderr)
        print("Run: python scripts/db/init_db.py && python scripts/db/sync.py", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    if args.query:
        fts_count = conn.execute("SELECT COUNT(*) FROM content_fts").fetchone()[0]
        if fts_count == 0:
            print("Warning: FTS index empty. Using LIKE fallback.", file=sys.stderr)
            print("Run: python scripts/db/sync.py to populate FTS.\n", file=sys.stderr)
            sql, params = build_like_query(args)
        else:
            sql, params = build_fts_query(args)
    else:
        if not any(v is not None for _, v in get_filters(args)):
            print("Provide a search query or at least one filter.", file=sys.stderr)
            sys.exit(1)
        sql, params = build_filter_query(args)

    rows = [dict(row) for row in conn.execute(sql, params).fetchall()]
    conn.close()

    if args.count:
        print(len(rows))
        return

    if not rows:
        print("No results found.")
        return

    if args.json_output:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(f"\n{len(rows)} result(s):\n")
        print(format_table(rows))
        print()


if __name__ == "__main__":
    main()
