#!/usr/bin/env python3
"""
One-time script to normalize Content/ folder structure.
Makes WS 2.0 identical to WS 1.0 and fills missing folders across all stages.

Usage:
    python scripts/normalize_structure.py --dry-run   # Preview changes
    python scripts/normalize_structure.py              # Execute changes
"""

import os
import sys
import argparse
from pathlib import Path

# Base path
CONTENT_DIR = Path(__file__).resolve().parent.parent / "Content"

# ─── Reference structure (from WS 1.0 Pre-Registration) ───

FEATURES = [
    "API", "Automation", "Brand_Ads", "Calendar", "Comments",
    "Custom_Fields", "Dark_Theme", "Dashboards", "File_Management",
    "Filters_Search", "Gantt_Chart", "Integrations", "Kanban",
    "Labels_Tags", "Migration", "Mobile_App", "Permissions",
    "Projects", "Reports", "Subtasks", "Task_Dependencies",
    "Tasks", "Teams", "Time_Material", "Time_Tracking", "User_Roles",
]

BUSINESS_TYPES = [
    "Agencies", "Architects", "Construction", "Consulting",
    "Education", "Enterprise", "Finance", "Government",
    "Healthcare", "Legal", "Manufacturing", "Media",
    "Non_Profits", "Other", "Retail", "Software", "Startups",
]

PAINS = [
    "Chat_Overload", "File_Loss", "Missed_Deadlines",
    "No_Transparency", "Task_Chaos", "Too_Many_Tools",
]

COMPETITORS = [
    "Asana", "Basecamp", "Bitrix24", "ClickUp",
    "Jira", "Monday", "Notion", "Telegram", "Trello",
]

PM_EDUCATION_FRAMEWORKS = [
    "Eisenhower_Matrix", "OKR_KPI", "RACI", "RAID", "SMART_Goals",
]

PM_EDUCATION_METHODOLOGIES = [
    "Agile", "Kanban_Method", "Lean", "Scrum", "Waterfall",
]

PM_EDUCATION_SKILLS = [
    "Management_Skills", "Organizational_Structure",
    "Remote_Hybrid_Work", "Team_Leadership",
]

PM_EDUCATION_STRATEGY = [
    "Decision_Making", "Goal_Setting", "Strategic_Planning",
]

# Content type subfolders per category
CONTENT_TYPE_DIRS_FEATURES = [
    "articles", "landings", "ads/static_ad", "ads/video_ad",
    "ads/lead_magnet", "videos", "smm", "SEO_Outreach",
]

CONTENT_TYPE_DIRS_BUSINESS = [
    "Case_Study", "Why_Worksection", "articles",
    "landings", "ads/static_ad", "ads/video_ad",
    "ads/lead_magnet", "videos", "smm",
]

CONTENT_TYPE_DIRS_PAINS = [
    "landings", "ads/static_ad", "ads/video_ad",
    "ads/lead_magnet", "videos", "smm",
]

CONTENT_TYPE_DIRS_COMPETITORS = [
    "articles", "landings", "ads/static_ad", "ads/video_ad",
    "ads/lead_magnet", "videos", "smm",
]

CONTENT_TYPE_DIRS_PM_EDUCATION = [
    "articles", "landings", "ads/static_ad", "ads/video_ad",
    "ads/lead_magnet", "videos", "smm",
]

# Products and stages
PRODUCTS = ["WS 1.0", "WS 2.0"]
STAGES = ["Pre-Registration", "Trial", "Success_Client"]

# WS 2.0 folder renames (old name → new name)
WS2_RENAMES = {
    "Pre-registration 2": "Pre-Registration",
    "Trial 2 ": "Trial",
    "Trial 2": "Trial",  # In case trailing space was stripped
    "Success 2": "Success_Client",
}

# Category folder renames (old name → new name)
CATEGORY_RENAMES = {
    "Business Type": "Business_Types",
    "Business Types": "Business_Types",
}


def collect_actions(dry_run=False):
    """Collect all actions (renames + creates) needed."""
    actions = {"renames": [], "creates": []}

    # ─── Step 1: Rename WS 2.0 stage folders ───
    ws2_dir = CONTENT_DIR / "WS 2.0"
    if ws2_dir.exists():
        for old_name, new_name in WS2_RENAMES.items():
            old_path = ws2_dir / old_name
            new_path = ws2_dir / new_name
            if old_path.exists() and not new_path.exists():
                actions["renames"].append((str(old_path), str(new_path)))

    # ─── Step 2: Rename category folders in WS 2.0 ───
    for product in PRODUCTS:
        product_dir = CONTENT_DIR / product
        if not product_dir.exists():
            continue
        for stage in STAGES:
            stage_dir = product_dir / stage
            if not stage_dir.exists():
                continue
            for old_name, new_name in CATEGORY_RENAMES.items():
                old_path = stage_dir / old_name
                new_path = stage_dir / new_name
                if old_path.exists() and not new_path.exists():
                    actions["renames"].append((str(old_path), str(new_path)))

    # ─── Step 3: Create missing structure ───
    for product in PRODUCTS:
        product_dir = CONTENT_DIR / product
        for stage in STAGES:
            stage_dir = product_dir / stage

            # Features
            for topic in FEATURES:
                for ct_dir in CONTENT_TYPE_DIRS_FEATURES:
                    path = stage_dir / "Features" / topic / ct_dir
                    if not path.exists():
                        actions["creates"].append(str(path))

            # Business_Types
            for topic in BUSINESS_TYPES:
                for ct_dir in CONTENT_TYPE_DIRS_BUSINESS:
                    path = stage_dir / "Business_Types" / topic / ct_dir
                    if not path.exists():
                        actions["creates"].append(str(path))

            # Pains
            for topic in PAINS:
                for ct_dir in CONTENT_TYPE_DIRS_PAINS:
                    path = stage_dir / "Pains" / topic / ct_dir
                    if not path.exists():
                        actions["creates"].append(str(path))

            # Competitors
            for topic in COMPETITORS:
                for ct_dir in CONTENT_TYPE_DIRS_COMPETITORS:
                    path = stage_dir / "Competitors" / topic / ct_dir
                    if not path.exists():
                        actions["creates"].append(str(path))

            # PM_Education — only in Pre-Registration
            if stage == "Pre-Registration":
                pm_base = stage_dir / "PM_Education"
                for topic in PM_EDUCATION_FRAMEWORKS:
                    for ct_dir in CONTENT_TYPE_DIRS_PM_EDUCATION:
                        path = pm_base / "Frameworks" / topic / ct_dir
                        if not path.exists():
                            actions["creates"].append(str(path))
                for topic in PM_EDUCATION_METHODOLOGIES:
                    for ct_dir in CONTENT_TYPE_DIRS_PM_EDUCATION:
                        path = pm_base / "Methodologies" / topic / ct_dir
                        if not path.exists():
                            actions["creates"].append(str(path))
                for topic in PM_EDUCATION_SKILLS:
                    for ct_dir in CONTENT_TYPE_DIRS_PM_EDUCATION:
                        path = pm_base / "Skills" / topic / ct_dir
                        if not path.exists():
                            actions["creates"].append(str(path))
                for topic in PM_EDUCATION_STRATEGY:
                    for ct_dir in CONTENT_TYPE_DIRS_PM_EDUCATION:
                        path = pm_base / "Strategy" / topic / ct_dir
                        if not path.exists():
                            actions["creates"].append(str(path))

    return actions


def execute_actions(actions, dry_run=False):
    """Execute or preview all actions."""
    prefix = "[DRY RUN] " if dry_run else ""

    # Renames first
    if actions["renames"]:
        print(f"\n{'='*60}")
        print(f"RENAMES ({len(actions['renames'])})")
        print(f"{'='*60}")
        for old_path, new_path in actions["renames"]:
            rel_old = os.path.relpath(old_path, CONTENT_DIR)
            rel_new = os.path.relpath(new_path, CONTENT_DIR)
            print(f"  {prefix}{rel_old}  →  {rel_new}")
            if not dry_run:
                os.rename(old_path, new_path)

    # Creates
    if actions["creates"]:
        # Group by product/stage/category for readable output
        by_category = {}
        for path in actions["creates"]:
            rel = os.path.relpath(path, CONTENT_DIR)
            parts = rel.split(os.sep)
            if len(parts) >= 3:
                key = os.sep.join(parts[:3])  # product/stage/category
            else:
                key = rel
            by_category.setdefault(key, []).append(rel)

        print(f"\n{'='*60}")
        print(f"NEW FOLDERS ({len(actions['creates'])} total)")
        print(f"{'='*60}")
        for category, paths in sorted(by_category.items()):
            print(f"\n  {category}/ ({len(paths)} folders)")
            # Show first 5 + count
            for p in paths[:5]:
                print(f"    {prefix}mkdir {p}")
            if len(paths) > 5:
                print(f"    ... and {len(paths) - 5} more")

            if not dry_run:
                for path in paths:
                    full_path = CONTENT_DIR / path
                    full_path.mkdir(parents=True, exist_ok=True)

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"  Renames: {len(actions['renames'])}")
    print(f"  New folders: {len(actions['creates'])}")
    if dry_run:
        print(f"\n  Run without --dry-run to execute these changes.")
    else:
        print(f"\n  Done! All changes applied.")


def verify_structure():
    """Verify that WS 1.0 and WS 2.0 have identical structure."""
    print(f"\n{'='*60}")
    print("VERIFICATION")
    print(f"{'='*60}")

    issues = []
    for stage in STAGES:
        ws1_stage = CONTENT_DIR / "WS 1.0" / stage
        ws2_stage = CONTENT_DIR / "WS 2.0" / stage

        if not ws1_stage.exists():
            issues.append(f"  MISSING: WS 1.0/{stage}/")
        if not ws2_stage.exists():
            issues.append(f"  MISSING: WS 2.0/{stage}/")
            continue

        # Compare categories
        categories = ["Features", "Business_Types", "Pains", "Competitors"]
        if stage == "Pre-Registration":
            categories.append("PM_Education")

        for cat in categories:
            ws1_cat = ws1_stage / cat
            ws2_cat = ws2_stage / cat
            if ws1_cat.exists() and ws2_cat.exists():
                ws1_topics = set(d.name for d in ws1_cat.iterdir() if d.is_dir())
                ws2_topics = set(d.name for d in ws2_cat.iterdir() if d.is_dir())
                missing_in_ws2 = ws1_topics - ws2_topics
                missing_in_ws1 = ws2_topics - ws1_topics
                if missing_in_ws2:
                    issues.append(f"  WS 2.0/{stage}/{cat} missing: {missing_in_ws2}")
                if missing_in_ws1:
                    issues.append(f"  WS 1.0/{stage}/{cat} missing: {missing_in_ws1}")
            elif not ws1_cat.exists():
                issues.append(f"  MISSING: WS 1.0/{stage}/{cat}/")
            elif not ws2_cat.exists():
                issues.append(f"  MISSING: WS 2.0/{stage}/{cat}/")

    if issues:
        print("  ISSUES FOUND:")
        for issue in issues:
            print(issue)
        return False
    else:
        print("  ✓ WS 1.0 and WS 2.0 have identical structure")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Normalize Content/ folder structure"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview changes without executing"
    )
    parser.add_argument(
        "--verify", action="store_true",
        help="Only verify current structure"
    )
    args = parser.parse_args()

    if not CONTENT_DIR.exists():
        print(f"ERROR: Content directory not found: {CONTENT_DIR}")
        sys.exit(1)

    print(f"Content directory: {CONTENT_DIR}")

    if args.verify:
        verify_structure()
        return

    actions = collect_actions()
    execute_actions(actions, dry_run=args.dry_run)

    if not args.dry_run:
        verify_structure()


if __name__ == "__main__":
    main()
