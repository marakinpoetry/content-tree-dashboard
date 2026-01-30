#!/usr/bin/env python3
"""
Generate Dashboard data.json by scanning Content/ folder
Runs locally or in GitHub Actions to keep dashboard in sync with Google Drive
"""

import os
import json
import re
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Any, Optional, Tuple

# Configuration
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CONTENT_DIR = PROJECT_DIR / "Content"
DASHBOARD_DIR = PROJECT_DIR / "Dashboard"
REPO_DATA_PATH = Path.home() / "data.json"  # For GitHub repo
DRIVE_URL_MAPPING_PATH = SCRIPT_DIR / "drive_url_mapping.json"

# Load Google Drive URL mapping (fallback for files without driveUrl in frontmatter)
DRIVE_URL_MAPPING = {}
if DRIVE_URL_MAPPING_PATH.exists():
    try:
        with open(DRIVE_URL_MAPPING_PATH, 'r', encoding='utf-8') as f:
            DRIVE_URL_MAPPING = json.load(f)
        print(f"Loaded {len(DRIVE_URL_MAPPING)} Google Drive URL mappings")
    except Exception as e:
        print(f"Warning: Could not load drive URL mapping: {e}")

# Stages configuration
STAGES = [
    "WS 1.0/Pre-Registration",
    "WS 1.0/Trial",
    "WS 1.0/Success_Client",
    "WS 2.0 Release"
]

# WS 1.0 sections
WS1_SECTIONS = ["Features", "Business_Types", "Competitors", "Pains", "PM_Education"]

# Content type detection from folder names
CONTENT_TYPE_MAP = {
    "articles": "Articles",
    "videos": "Videos",
    "video": "Videos",
    "landings": "Landings",
    "landing": "Landings",
    "ads": "Ads",
    "static_ad": "Static Ads",
    "static_ads": "Static Ads",
    "static ads": "Static Ads",
    "video_ad": "Ads",
    "video_ads": "Ads",
    "video ads": "Ads",
    "smm": "SMM",
    "lead_magnet": "Lead Magnets",
    "lead_magnets": "Lead Magnets",
    "lead magnets": "Lead Magnets",
    "cases": "Other",
    "case_study": "Other",
    "guides": "Other",
    "tutorials": "Other",
    "pr&media": "Other",
    "product hunt kit": "Other",
}

# Language detection from filename suffix
LANGUAGE_MAP = {
    "_uk": "Ukrainian",
    "_ua": "Ukrainian",
    "_en": "English",
    "_ru": "Russian",
    "_pl": "Polish",
    "_de": "German",
    "_fr": "French",
    "_es": "Spanish",
}

# File extensions to include
VALID_EXTENSIONS = {".md", ".txt", ".csv", ".docx"}

# Folders to exclude
EXCLUDE_FOLDERS = {"Hubs", ".git", "__pycache__", ".DS_Store"}


def detect_language(filename: str) -> str:
    """Detect language from filename suffix"""
    name_lower = filename.lower()
    for suffix, lang in LANGUAGE_MAP.items():
        if suffix in name_lower:
            return lang
    return "Unknown"


def detect_content_type(path_parts: List[str]) -> str:
    """Detect content type from folder path"""
    for part in reversed(path_parts):
        part_lower = part.lower()
        if part_lower in CONTENT_TYPE_MAP:
            return CONTENT_TYPE_MAP[part_lower]
    return "Other"


def detect_stage(rel_path: str) -> Optional[str]:
    """Detect stage from relative path"""
    for stage in STAGES:
        if rel_path.startswith(stage):
            return stage
    return None


def detect_section(rel_path: str, stage: str) -> str:
    """Detect section (Features, Business_Types, etc.) from path"""
    # Remove stage prefix
    after_stage = rel_path[len(stage):].lstrip("/")
    parts = after_stage.split("/")

    if parts and parts[0] in WS1_SECTIONS:
        return parts[0]

    # For WS 2.0, use the first folder as section
    if stage == "WS 2.0 Release" and parts:
        return parts[0]

    return stage.split("/")[-1]  # Default to stage name


def detect_feature(rel_path: str, section: str) -> str:
    """Detect feature/subcategory from path"""
    parts = rel_path.split("/")
    try:
        section_idx = parts.index(section)
        if section_idx + 1 < len(parts):
            return parts[section_idx + 1]
    except ValueError:
        pass
    return section


def extract_frontmatter(file_path: Path) -> Dict[str, Any]:
    """Extract YAML frontmatter from markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(4096)  # Read first 4KB

        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            return yaml.safe_load(match.group(1)) or {}
    except Exception:
        pass
    return {}


def extract_status(metadata: Dict, filename: str) -> str:
    """Extract status from metadata or filename"""
    # Check frontmatter
    status = metadata.get("status", "")
    if status:
        status_map = {
            "published": "Published",
            "approved": "Approved",
            "review": "Review",
            "idea": "Idea/Brief",
            "brief": "Idea/Brief",
            "blocked": "Blocked",
            "active": "Published",
            "draft": "Idea/Brief",
        }
        return status_map.get(status.lower(), "Unknown")

    # Check hierarchical_tags
    tags = metadata.get("hierarchical_tags", {})
    attrs = tags.get("content_attributes", {})
    if attrs.get("status"):
        return attrs.get("status")

    return "Idea/Brief"  # Default


def extract_snippet(file_path: Path) -> str:
    """Extract first line of content as snippet"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(2048)

        # Skip frontmatter
        if content.startswith("---"):
            match = re.match(r'^---\s*\n.*?\n---\s*\n(.*)$', content, re.DOTALL)
            if match:
                content = match.group(1)

        # Get first non-empty line
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                return line[:100]
    except Exception:
        pass
    return ""


def extract_keywords(filename: str) -> List[str]:
    """Extract keywords from filename"""
    # Remove extension
    name = Path(filename).stem
    # Split by underscores, dashes, spaces
    words = re.split(r'[_\-\s]+', name.lower())
    # Filter short words and common suffixes
    keywords = [w for w in words if len(w) > 2 and w not in {'md', 'txt', 'en', 'uk', 'ru', 'pl'}]
    return keywords[:10]


def build_folder_tree(folder_path: Path, rel_base: str = "") -> Dict[str, Any]:
    """Build recursive folder tree structure"""
    name = folder_path.name or "root"
    rel_path = rel_base

    tree = {
        "name": name,
        "path": rel_path or ".",
        "file_count": 0,
        "children": [],
        "files": [],
        "is_empty": True
    }

    if not folder_path.exists():
        return tree

    try:
        entries = sorted(folder_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
    except PermissionError:
        return tree

    for entry in entries:
        if entry.name in EXCLUDE_FOLDERS or entry.name.startswith('.'):
            continue

        if entry.is_dir():
            child_rel = f"{rel_path}/{entry.name}" if rel_path else entry.name
            child_tree = build_folder_tree(entry, child_rel)
            tree["children"].append(child_tree)
            tree["file_count"] += child_tree["file_count"]
        elif entry.is_file() and entry.suffix.lower() in VALID_EXTENSIONS:
            tree["files"].append({
                "name": entry.name,
                "size": entry.stat().st_size,
                "modified": datetime.fromtimestamp(entry.stat().st_mtime).isoformat()
            })
            tree["file_count"] += 1

    tree["is_empty"] = tree["file_count"] == 0
    return tree


def count_folders(folder_path: Path) -> Tuple[int, int, List[str]]:
    """Count total folders, filled folders, and list empty folders"""
    total = 0
    filled = 0
    empty_list = []

    for root, dirs, files in os.walk(folder_path):
        # Skip excluded folders
        dirs[:] = [d for d in dirs if d not in EXCLUDE_FOLDERS and not d.startswith('.')]

        rel_path = os.path.relpath(root, folder_path)
        if rel_path == '.':
            continue

        total += 1
        content_files = [f for f in files if Path(f).suffix.lower() in VALID_EXTENSIONS]

        if content_files:
            filled += 1
        else:
            # Only add leaf folders (no subdirectories) as empty
            if not dirs:
                empty_list.append(rel_path)

    return total, filled, empty_list


def scan_files(content_dir: Path) -> List[Dict[str, Any]]:
    """Scan all content files and extract metadata"""
    files = []
    file_idx = defaultdict(int)

    for root, dirs, filenames in os.walk(content_dir):
        # Skip excluded folders
        dirs[:] = [d for d in dirs if d not in EXCLUDE_FOLDERS and not d.startswith('.')]

        for filename in filenames:
            if not any(filename.lower().endswith(ext) for ext in VALID_EXTENSIONS):
                continue

            file_path = Path(root) / filename
            rel_path = str(file_path.relative_to(content_dir))
            path_parts = rel_path.split(os.sep)

            # Detect stage
            stage = detect_stage(rel_path)
            if not stage:
                continue

            # Generate unique ID
            file_idx[stage] += 1
            file_id = f"{stage}_{file_idx[stage]}"

            # Extract metadata
            frontmatter = extract_frontmatter(file_path)
            stat = file_path.stat()

            section = detect_section(rel_path, stage)
            feature = detect_feature(rel_path, section)
            content_type = detect_content_type(path_parts)
            language = detect_language(filename)
            status = extract_status(frontmatter, filename)

            # Build display name
            display_name = Path(filename).stem.replace('_', ' ').replace('-', ' ').title()

            file_entry = {
                "id": file_id,
                "name": filename,
                "display_name": display_name,
                "path": rel_path,
                "full_path": str(file_path),
                "stage": stage,
                "section": section,
                "feature": feature,
                "content_type": content_type,
                "language": language,
                "status": status,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "keywords": extract_keywords(filename),
                "snippet": extract_snippet(file_path),
            }

            # Add drive URL if available (from frontmatter or mapping)
            drive_url = frontmatter.get("driveUrl") or frontmatter.get("drive_url")
            if not drive_url:
                # Try to get from Google Drive mapping
                drive_url = DRIVE_URL_MAPPING.get(rel_path)
            if drive_url:
                file_entry["driveUrl"] = drive_url

            files.append(file_entry)

    return files


def calculate_growth_trend(files: List[Dict]) -> Dict[str, Any]:
    """Calculate growth trend based on file modification dates"""
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    last_week = 0
    last_month = 0

    for f in files:
        try:
            modified = datetime.fromisoformat(f["modified"])
            if modified > week_ago:
                last_week += 1
            if modified > month_ago:
                last_month += 1
        except:
            pass

    weekly_avg = round(last_month / 4.3, 1) if last_month else 0

    return {
        "last_week": last_week,
        "last_month": last_month,
        "weekly_avg": weekly_avg
    }


def calculate_gaps(files: List[Dict], stages_detail: Dict) -> List[Dict]:
    """Calculate content gaps - simplified version"""
    gaps = []

    # Expected content types per section
    expected_types = ["Articles", "Videos", "Landings"]

    for stage in ["WS 1.0/Pre-Registration", "WS 1.0/Trial", "WS 1.0/Success_Client"]:
        stage_files = [f for f in files if f["stage"] == stage]
        stage_detail = stages_detail.get(stage, {})

        for section in WS1_SECTIONS:
            section_files = [f for f in stage_files if f["section"] == section]

            # Group by feature
            features = defaultdict(list)
            for f in section_files:
                features[f["feature"]].append(f)

            # Check each feature for gaps
            for feature, feature_files in features.items():
                content_types = set(f["content_type"] for f in feature_files)

                for expected in expected_types:
                    if expected not in content_types:
                        # Calculate priority
                        priority = 70 if stage == "WS 1.0/Trial" else 60 if stage == "WS 1.0/Pre-Registration" else 50
                        if section == "Features":
                            priority += 10

                        gaps.append({
                            "path": f"{stage}/{section}/{feature}",
                            "type": "content_gap",
                            "stage": stage,
                            "section": section,
                            "feature": feature,
                            "content_type": expected,
                            "severity": "high" if priority >= 70 else "medium",
                            "priority_score": priority,
                            "fill_rate": 0.0,
                            "current_count": 0,
                            "ideal_count": 3,
                            "message": f"{feature}: {expected} gap (0/3)",
                        })

    # Sort by priority
    gaps.sort(key=lambda x: -x["priority_score"])
    return gaps[:50]  # Return top 50 gaps


def calculate_ws2_gaps(files: List[Dict]) -> Tuple[List[Dict], Dict]:
    """Calculate WS 2.0 gaps based on content plan (MD files only)"""
    plan_path = SCRIPT_DIR / "ws2_content_plan.json"
    if not plan_path.exists():
        return [], {}

    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = json.load(f)

    gaps = []
    section_progress = {}

    # Only count .md files as content
    ws2_md_files = [f for f in files
                    if f["stage"] == "WS 2.0 Release"
                    and f["path"].endswith(".md")]

    # Count other files (not .md)
    ws2_other_files = [f for f in files
                       if f["stage"] == "WS 2.0 Release"
                       and not f["path"].endswith(".md")]

    for section, config in plan["categories"].items():
        required = config["required"]

        # Count MD files matching this section
        current = len([f for f in ws2_md_files
                      if section.lower().replace(" ", "") in
                         f["section"].lower().replace(" ", "")])

        section_progress[section] = {
            "current": current,
            "required": required,
            "fill_rate": min(100, round(current / required * 100, 1))
                        if required > 0 else 100
        }

        if current < required:
            gaps.append({
                "path": f"WS 2.0 Release/{section}",
                "type": "ws2_content_gap",
                "stage": "WS 2.0 Release",
                "section": section,
                "severity": "high" if current == 0 else "medium",
                "priority_score": 85 if current == 0 else 70,
                "current_count": current,
                "required_count": required,
                "missing_count": required - current,
                "message": f"{section}: {current}/{required}"
            })

    # Track other files (no requirement, just count)
    section_progress["other files"] = {
        "current": len(ws2_other_files),
        "required": 0,
        "fill_rate": 100
    }

    return gaps, section_progress


def generate_smart_recommendations(gaps: List[Dict], files: List[Dict]) -> Dict[str, Any]:
    """Generate smart recommendations based on gaps"""
    top_gaps = gaps[:5]

    return {
        "top_priorities": [
            {
                "rank": i + 1,
                "title": f"{g['feature']} - {g['content_type']}",
                "stage": g["stage"],
                "path": g["path"],
                "priority_score": g["priority_score"],
                "impact": "Critical" if g["priority_score"] >= 80 else "High" if g["priority_score"] >= 60 else "Medium",
                "reasons": [f"Missing {g['content_type']} content for {g['feature']}"],
            }
            for i, g in enumerate(top_gaps)
        ],
        "quick_wins": [],
        "strategic_priorities": [],
        "balance_analysis": [
            {
                "type": "resource_allocation",
                "message": "Focus on Trial stage content to improve activation",
                "suggestion": "Allocate 40% to Trial, 35% to Pre-Registration, 25% to others"
            }
        ]
    }


def generate_dashboard_data() -> Dict[str, Any]:
    """Main function to generate complete dashboard data"""
    print(f"Scanning content folder: {CONTENT_DIR}")

    # Scan all files
    files = scan_files(CONTENT_DIR)
    print(f"Found {len(files)} content files")

    # Calculate aggregations
    by_stage = defaultdict(int)
    by_content_type = defaultdict(int)
    by_language = defaultdict(int)
    by_status = defaultdict(int)

    for f in files:
        by_stage[f["stage"]] += 1
        by_content_type[f["content_type"]] += 1
        by_language[f["language"]] += 1
        by_status[f["status"]] += 1

    # Build stages_detail
    stages_detail = {}
    total_folders = 0
    total_filled = 0
    all_empty_folders = []

    for stage in STAGES:
        stage_path = CONTENT_DIR / stage.replace("/", os.sep)
        if not stage_path.exists():
            continue

        stage_files = [f for f in files if f["stage"] == stage]
        folders, filled, empty = count_folders(stage_path)

        total_folders += folders
        total_filled += filled
        all_empty_folders.extend([f"{stage}/{e}" for e in empty[:20]])  # Limit empty folders

        # By section
        by_section = defaultdict(int)
        for f in stage_files:
            by_section[f["section"]] += 1

        # Recent changes (top 3)
        recent = sorted(stage_files, key=lambda x: x["modified"], reverse=True)[:3]

        # Folder tree
        folder_tree = build_folder_tree(stage_path)
        folder_tree["name"] = stage.split("/")[-1]

        # Calculate fill rate
        fill_rate = round((filled / folders * 100), 1) if folders > 0 else 0

        stages_detail[stage] = {
            "total_files": len(stage_files),
            "total_folders": folders,
            "filled_folders": filled,
            "empty_folders_count": folders - filled,
            "fill_rate": fill_rate,
            "by_section": dict(by_section),
            "by_subsection": {},
            "empty_folders": empty[:20],
            "recent_changes": [
                {
                    "path": f["path"],
                    "name": f["name"],
                    "section": f["section"],
                    "content_type": f["content_type"],
                    "language": f["language"],
                    "status": f["status"],
                    "modified": f["modified"],
                    "size": f["size"],
                }
                for f in recent
            ],
            "folder_tree": folder_tree,
        }

        # Add section_progress for WS 2.0
        if stage == "WS 2.0 Release":
            stages_detail[stage]["section_progress"] = {
                section: {
                    "current": count,
                    "required": max(count, 10),
                    "fill_rate": min(100, round(count / max(count, 10) * 100, 1))
                }
                for section, count in by_section.items()
            }

    # Calculate gaps
    gaps = calculate_gaps(files, stages_detail)

    # Add WS 2.0 specific gaps
    ws2_gaps, ws2_progress = calculate_ws2_gaps(files)
    gaps.extend(ws2_gaps)

    # Update WS 2.0 section_progress
    if "WS 2.0 Release" in stages_detail:
        stages_detail["WS 2.0 Release"]["section_progress"] = ws2_progress

    # Build final data structure
    total_files = len(files)
    fill_rate = round((total_filled / total_folders * 100), 1) if total_folders > 0 else 0
    published_count = by_status.get("Published", 0) + by_status.get("Approved", 0)

    data = {
        "metadata": {
            "last_update": datetime.now().isoformat(),
            "total_files": total_files,
            "total_folders": total_folders,
            "filled_folders": total_filled,
            "empty_folders": total_folders - total_filled,
            "fill_rate": fill_rate,
            "target_files": "Fill all folders",
            "coverage_percent": fill_rate,
            "smart_analysis_enabled": True,
            "published_count": published_count,
            "not_published_count": total_files - published_count,
        },
        "by_stage": dict(by_stage),
        "by_content_type": dict(by_content_type),
        "by_language": dict(by_language),
        "by_status": dict(by_status),
        "growth_trend": calculate_growth_trend(files),
        "gaps": gaps,
        "search_index": files,
        "smart_recommendations": generate_smart_recommendations(gaps, files),
        "stages_detail": stages_detail,
    }

    return data


def save_data(data: Dict[str, Any]):
    """Save data.json to all required locations"""
    # Dashboard folder
    dashboard_path = DASHBOARD_DIR / "data.json"
    dashboard_path.parent.mkdir(parents=True, exist_ok=True)

    with open(dashboard_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved: {dashboard_path}")

    # Repo root (for GitHub Pages)
    if REPO_DATA_PATH.parent.exists():
        with open(REPO_DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved: {REPO_DATA_PATH}")


def main():
    print("=" * 50)
    print("Dashboard Data Generator")
    print("=" * 50)

    data = generate_dashboard_data()
    save_data(data)

    print("\nSummary:")
    print(f"  Total files: {data['metadata']['total_files']}")
    print(f"  Total folders: {data['metadata']['total_folders']}")
    print(f"  Fill rate: {data['metadata']['fill_rate']}%")
    print(f"  Gaps found: {len(data['gaps'])}")
    print("\nDone!")


if __name__ == "__main__":
    main()
