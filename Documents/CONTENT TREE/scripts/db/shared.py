"""
Shared detection functions for Content Tree database.
Parses file paths and content to extract normalized metadata.
"""

import os
import re
from pathlib import Path
from typing import Any, Dict, Optional

from scripts.db.constants import (
    CATEGORY_ALIASES,
    CONTENT_TYPE_ALIASES,
    EXCLUDED_DIRS,
    EXTENSION_CONTENT_TYPE,
    LANGUAGE_ALIASES,
    STAGE_ALIASES,
    STATUS_ALIASES,
)


def parse_content_path(rel_path: str) -> Dict[str, Optional[str]]:
    """
    Parse a relative path (from Content/) into structured metadata.

    Examples:
        WS 1.0/Pre-Registration/Features/Kanban/articles/file.md
        → product=WS 1.0, stage=Pre-Registration, category=Features,
          topic=Kanban, content_type=article

        WS 2.0 Release/articles/file.md
        → product=WS 2.0 Release, stage=None, category=None,
          topic=None, content_type=article
    """
    parts = Path(rel_path).parts
    result = {
        "product": None,
        "stage": None,
        "category": None,
        "topic": None,
    }

    if not parts:
        return result

    # Product
    product_folder = parts[0]
    if product_folder in ("WS 1.0", "WS 2.0"):
        result["product"] = product_folder
    elif product_folder == "WS 2.0 Release":
        result["product"] = "WS 2.0 Release"
    else:
        return result  # Unknown (Hubs, etc.)

    # WS 2.0 Release: flat structure, no stage/category/topic
    if result["product"] == "WS 2.0 Release":
        return result

    # WS 1.0 / WS 2.0: hierarchical structure
    if len(parts) >= 2:
        stage_raw = parts[1].strip()
        result["stage"] = STAGE_ALIASES.get(stage_raw) or STAGE_ALIASES.get(parts[1])

    if len(parts) >= 3:
        cat_raw = parts[2]
        result["category"] = CATEGORY_ALIASES.get(cat_raw)

    if len(parts) >= 4:
        potential_topic = parts[3]
        # Check if this is a content type folder (not a topic)
        if potential_topic.lower() in CONTENT_TYPE_ALIASES:
            pass  # No topic, content_type will be detected separately
        else:
            result["topic"] = potential_topic

    return result


def detect_content_type(rel_path: str, filename: str) -> str:
    """
    Detect content type from path folders and file extension.
    Deepest matching folder wins. Falls back to file extension.
    """
    parts = Path(rel_path).parts
    ct = None

    # Scan folders (deepest match wins)
    for part in parts[:-1]:  # exclude filename
        alias = CONTENT_TYPE_ALIASES.get(part) or CONTENT_TYPE_ALIASES.get(part.lower())
        if alias:
            ct = alias

    # Generic "ad" from ads/ folder → disambiguate
    if ct == "ad":
        ext = os.path.splitext(filename)[1].lower()
        ext_ct = EXTENSION_CONTENT_TYPE.get(ext)
        if ext_ct in ("static_ad", "video", "video_ad"):
            ct = ext_ct
        else:
            ct = "static_ad"  # default for ads/

    # No folder match → check file extension
    if ct is None:
        ext = os.path.splitext(filename)[1].lower()
        ext_ct = EXTENSION_CONTENT_TYPE.get(ext)
        if ext_ct:
            ct = ext_ct
        else:
            ct = "other"

    return ct


def detect_language(filename: str) -> Optional[str]:
    """
    Detect language from filename suffix.
    Examples: file_ua.md → 'ua', article_en.md → 'en'
    """
    stem = Path(filename).stem.lower()
    # Check suffix after last underscore or dash
    for sep in ("_", "-"):
        if sep in stem:
            suffix = stem.rsplit(sep, 1)[-1]
            lang = LANGUAGE_ALIASES.get(suffix)
            if lang:
                return lang
    return None


def extract_frontmatter(file_path: str) -> Dict[str, Any]:
    """Extract YAML frontmatter from a markdown file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(4096)
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if match:
            import yaml
            return yaml.safe_load(match.group(1)) or {}
    except Exception:
        pass
    return {}


def extract_status(frontmatter: Dict, filename: str) -> str:
    """Extract and normalize status from frontmatter or filename."""
    # From frontmatter status field
    status = frontmatter.get("status", "")
    if status:
        return STATUS_ALIASES.get(status.lower(), "draft")

    # From hierarchical_tags
    tags = frontmatter.get("hierarchical_tags", {})
    if isinstance(tags, dict):
        attrs = tags.get("content_attributes", {})
        if isinstance(attrs, dict) and attrs.get("status"):
            return STATUS_ALIASES.get(attrs["status"].lower(), "draft")

    return "draft"


def extract_title(file_path: str, frontmatter: Dict) -> Optional[str]:
    """Extract title from frontmatter or first heading."""
    # From frontmatter
    title = frontmatter.get("title")
    if title:
        return str(title).strip()

    # From first markdown heading
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(4096)
        # Skip frontmatter
        if content.startswith("---"):
            m = re.match(r"^---\s*\n.*?\n---\s*\n(.*)", content, re.DOTALL)
            if m:
                content = m.group(1)
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("#"):
                return line.lstrip("#").strip()
    except Exception:
        pass
    return None


def count_words(file_path: str) -> int:
    """Count words in a text file (skipping frontmatter)."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Skip frontmatter
        if content.startswith("---"):
            m = re.match(r"^---\s*\n.*?\n---\s*\n(.*)", content, re.DOTALL)
            if m:
                content = m.group(1)
        return len(content.split())
    except Exception:
        return 0


def extract_body(file_path: str, max_chars: int = 50_000) -> str:
    """Extract body text from a .md file, stripping frontmatter.
    Returns up to max_chars of text. Empty string for non-.md files."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext != ".md":
        return ""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(max_chars + 5000)
        if content.startswith("---"):
            m = re.match(r"^---\s*\n.*?\n---\s*\n(.*)", content, re.DOTALL)
            if m:
                content = m.group(1)
        return content[:max_chars]
    except Exception:
        return ""


def should_skip(name: str) -> bool:
    """Check if a file/folder should be skipped."""
    return name in EXCLUDED_DIRS or name.startswith(".")
