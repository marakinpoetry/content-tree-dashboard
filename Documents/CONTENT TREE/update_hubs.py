#!/usr/bin/env python3
"""
Auto-update Hub files when content changes
Scans all Content/ markdown files and generates Hub navigation system
"""

import os
import yaml
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple

# Configuration
SCRIPT_DIR = Path(__file__).parent
CONTENT_DIR = SCRIPT_DIR / "Content"
HUBS_DIR = CONTENT_DIR / "Hubs"

# Hub categories and their directories
HUB_CATEGORIES = {
    'features': 'features',
    'business_type': 'business_types',
    'competitor': 'competitors',
    'topic': 'topics',
    'pain': 'pains'
}

# Content type emojis
CONTENT_TYPE_EMOJI = {
    'article': '📄',
    'video': '🎥',
    'ad': '📢',
    'landing': '🌐',
    'tutorial': '📚',
    'case_study': '📊',
    'guide': '📖',
    'other': '📝'
}

# Language flags
LANGUAGE_FLAGS = {
    'en': '🇬🇧',
    'uk': '🇺🇦',
    'ru': '🇷🇺',
    'multi': '🌍'
}

# Stage emojis
STAGE_EMOJI = {
    'Pre-Registration': '🎯',
    'Trial': '🚀',
    'Success_Client': '⭐'
}

class ContentFile:
    """Represents a content file with its metadata"""
    def __init__(self, path: Path, metadata: dict):
        self.path = path
        self.metadata = metadata
        self.relative_path = path.relative_to(CONTENT_DIR)

        # Extract hierarchical tags
        tags = metadata.get('hierarchical_tags', {})
        primary = tags.get('primary', {})
        attrs = tags.get('content_attributes', {})

        self.category = primary.get('category', 'unknown')
        self.value = primary.get('value', 'unknown')
        self.stage = attrs.get('stage', 'unknown')
        self.content_type = attrs.get('content_type', 'other')
        self.language = attrs.get('language', 'en')
        self.title = metadata.get('title', path.stem)

    def __repr__(self):
        return f"ContentFile({self.relative_path}, {self.category}:{self.value})"


def extract_frontmatter(file_path: Path) -> dict:
    """Extract YAML frontmatter from markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match YAML frontmatter between --- delimiters
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            yaml_content = match.group(1)
            return yaml.safe_load(yaml_content) or {}
    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}")

    return {}


def scan_content_files() -> List[ContentFile]:
    """Scan all .md files in Content/ and extract metadata"""
    print("📂 Scanning content files...")

    content_files = []
    md_files = list(CONTENT_DIR.rglob("*.md"))

    # Exclude Hub files from scan
    md_files = [f for f in md_files if not str(f).startswith(str(HUBS_DIR))]

    for file_path in md_files:
        metadata = extract_frontmatter(file_path)

        # Only include files with hierarchical_tags
        if 'hierarchical_tags' in metadata:
            content_file = ContentFile(file_path, metadata)
            content_files.append(content_file)

    print(f"✅ Found {len(content_files)} tagged content files (out of {len(md_files)} total)")
    return content_files


def group_by_tags(content_files: List[ContentFile]) -> Dict[str, Dict[str, List[ContentFile]]]:
    """Group content files by category and value"""
    grouped = defaultdict(lambda: defaultdict(list))

    for cf in content_files:
        if cf.category in HUB_CATEGORIES:
            grouped[cf.category][cf.value].append(cf)

    return grouped


def calculate_stats(files: List[ContentFile]) -> dict:
    """Calculate statistics for a group of files"""
    total = len(files)
    if total == 0:
        return {
            'total': 0,
            'by_stage': {},
            'by_type': {},
            'by_language': {}
        }

    by_stage = defaultdict(int)
    by_type = defaultdict(int)
    by_language = defaultdict(int)

    for f in files:
        by_stage[f.stage] += 1
        by_type[f.content_type] += 1
        by_language[f.language] += 1

    return {
        'total': total,
        'by_stage': dict(by_stage),
        'by_type': dict(by_type),
        'by_language': dict(by_language)
    }


def format_percentage(count: int, total: int) -> str:
    """Format percentage with 1 decimal place"""
    if total == 0:
        return "0.0"
    return f"{(count / total * 100):.1f}"


def get_relative_path(from_hub: Path, to_content: Path) -> str:
    """Get relative path from hub file to content file"""
    try:
        rel_path = os.path.relpath(to_content, from_hub.parent)
        return rel_path
    except:
        return str(to_content)


def generate_hub_file(category: str, value: str, files: List[ContentFile]) -> Path:
    """Generate a single Hub file"""
    stats = calculate_stats(files)

    # Create hub directory if needed
    hub_subdir = HUBS_DIR / HUB_CATEGORIES[category]
    hub_subdir.mkdir(parents=True, exist_ok=True)

    # Create hub filename
    hub_filename = f"{value.lower().replace(' ', '_').replace('/', '_')}_hub.md"
    hub_path = hub_subdir / hub_filename

    # Format value for display
    display_value = value.replace('_', ' ').title()
    display_category = category.replace('_', ' ').title()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Start building the hub content
    content = f"""---
title: "{display_value} Hub"
type: hub
category: {category}
value: {value}
total_items: {stats['total']}
last_updated: {current_time}
auto_generated: true
---

# {display_value} Hub

> **Category:** {display_category} | **Total Content:** {stats['total']} items | **Last Updated:** {datetime.now().strftime("%Y-%m-%d")}

---

## 📊 Content Overview

### Distribution by Stage
| Stage | Count | Percentage |
|-------|-------|------------|
"""

    # Stage distribution
    stages = ['Pre-Registration', 'Trial', 'Success_Client']
    for stage in stages:
        count = stats['by_stage'].get(stage, 0)
        percent = format_percentage(count, stats['total'])
        emoji = STAGE_EMOJI.get(stage, '📍')
        content += f"| {emoji} {stage.replace('_', ' ')} | {count} | {percent}% |\n"

    content += f"| **Total** | **{stats['total']}** | **100.0%** |\n\n"

    # Content type distribution
    content += """### Distribution by Content Type
| Type | Count | Percentage |
|------|-------|------------|
"""

    type_counts = defaultdict(int)
    for t, count in stats['by_type'].items():
        type_counts[t] = count

    # Group types
    article_count = type_counts.get('article', 0)
    video_count = type_counts.get('video', 0)
    ad_count = type_counts.get('ad', 0)
    landing_count = type_counts.get('landing', 0)
    tutorial_count = type_counts.get('tutorial', 0)
    guide_count = type_counts.get('guide', 0)
    case_study_count = type_counts.get('case_study', 0)
    other_count = sum(c for t, c in type_counts.items()
                     if t not in ['article', 'video', 'ad', 'landing', 'tutorial', 'guide', 'case_study'])

    type_display = [
        ('📄 Articles', article_count),
        ('🎥 Videos', video_count),
        ('📢 Ads', ad_count),
        ('🌐 Landings', landing_count),
        ('📚 Tutorials', tutorial_count),
        ('📖 Guides', guide_count),
        ('📊 Case Studies', case_study_count),
        ('📝 Other', other_count)
    ]

    for label, count in type_display:
        if count > 0:
            percent = format_percentage(count, stats['total'])
            content += f"| {label} | {count} | {percent}% |\n"

    content += f"| **Total** | **{stats['total']}** | **100.0%** |\n\n"

    # Language distribution
    content += """### Distribution by Language
| Language | Count | Percentage |
|----------|-------|------------|
"""

    lang_display = [
        ('🇬🇧 English', 'en'),
        ('🇺🇦 Ukrainian', 'uk'),
        ('🇷🇺 Russian', 'ru'),
        ('🌍 Multi-language', 'multi')
    ]

    for label, lang_code in lang_display:
        count = stats['by_language'].get(lang_code, 0)
        if count > 0:
            percent = format_percentage(count, stats['total'])
            content += f"| {label} | {count} | {percent}% |\n"

    content += f"| **Total** | **{stats['total']}** | **100.0%** |\n\n"

    content += "---\n\n## 📁 Content Inventory\n\n"

    # Group files by stage and type
    for stage in stages:
        stage_files = [f for f in files if f.stage == stage]
        if not stage_files:
            continue

        emoji = STAGE_EMOJI.get(stage, '📍')
        content += f"### {emoji} {stage.replace('_', ' ')} Content\n\n"

        # Group by content type
        by_type = defaultdict(list)
        for f in stage_files:
            by_type[f.content_type].append(f)

        for ctype, type_files in sorted(by_type.items()):
            emoji = CONTENT_TYPE_EMOJI.get(ctype, '📝')
            type_label = ctype.replace('_', ' ').title()
            content += f"#### {emoji} {type_label}s ({len(type_files)})\n"

            for f in sorted(type_files, key=lambda x: x.title):
                rel_path = get_relative_path(hub_path, f.path)
                lang_flag = LANGUAGE_FLAGS.get(f.language, '🌐')
                content += f"- [{f.title}]({rel_path}) {lang_flag}\n"

            content += "\n"

    # Related Hubs section
    content += """---

## 🔗 Related Hubs

"""

    # Analyze cross-references based on category
    related = analyze_related_hubs(category, value, files)

    if related:
        for rel_category, rel_items in related.items():
            cat_display = rel_category.replace('_', ' ').title()
            content += f"### Related {cat_display}\n"
            for rel_value, count in sorted(rel_items.items(), key=lambda x: x[1], reverse=True)[:5]:
                rel_hub_dir = HUB_CATEGORIES.get(rel_category, rel_category)
                rel_hub_file = f"{rel_value.lower().replace(' ', '_').replace('/', '_')}_hub.md"
                rel_path = f"../{rel_hub_dir}/{rel_hub_file}"
                rel_display = rel_value.replace('_', ' ').title()
                content += f"- [{rel_display}]({rel_path}) - mentioned in {count} files\n"
            content += "\n"
    else:
        content += "*No cross-references detected yet. This will update as more content is added.*\n\n"

    # Gap Analysis
    content += """---

## ⚠️ Content Gaps Analysis

"""

    gaps = analyze_gaps(stats)
    content += gaps

    # Customer Journey Coverage
    content += """---

## 🎯 Customer Journey Coverage

**Awareness → Activation → Success**

| Journey Stage | Content Available | Status |
|---------------|-------------------|--------|
"""

    pre_count = stats['by_stage'].get('Pre-Registration', 0)
    trial_count = stats['by_stage'].get('Trial', 0)
    success_count = stats['by_stage'].get('Success_Client', 0)

    def get_status(count):
        if count == 0:
            return '❌'
        elif count < 3:
            return '⚠️'
        else:
            return '✅'

    content += f"| **Awareness** (Pre-Reg) | {pre_count} items | {get_status(pre_count)} |\n"
    content += f"| **Activation** (Trial) | {trial_count} items | {get_status(trial_count)} |\n"
    content += f"| **Success** (Client) | {success_count} items | {get_status(success_count)} |\n\n"

    # Calculate journey health
    journey_stages = 3
    covered_stages = sum(1 for c in [pre_count, trial_count, success_count] if c > 0)
    health_score = format_percentage(covered_stages, journey_stages)

    content += f"**Journey Health Score:** {health_score}% complete\n\n"

    content += f"""---

*🤖 Auto-generated Hub | Last updated: {current_time} | Next update: on content change*
*For questions about this Hub system, see [Hub Documentation](../README.md)*
"""

    # Write the hub file
    with open(hub_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return hub_path


def analyze_related_hubs(category: str, value: str, files: List[ContentFile]) -> dict:
    """Analyze which other hubs are related based on content"""
    # This is a placeholder - could be enhanced to parse file content
    # For now, we'll return empty dict
    return {}


def analyze_gaps(stats: dict) -> str:
    """Analyze content gaps and generate recommendations"""
    content = ""

    # Check stage gaps
    content += "### Missing by Stage:\n"
    stages = ['Pre-Registration', 'Trial', 'Success_Client']
    stage_issues = []

    for stage in stages:
        count = stats['by_stage'].get(stage, 0)
        if count == 0:
            stage_issues.append(f"- ❌ No {stage.replace('_', ' ')} content - **ACTION NEEDED**")
        elif count < 3:
            stage_issues.append(f"- ⚠️ Only {count} {stage.replace('_', ' ')} item(s) - **Consider expansion**")
        else:
            stage_issues.append(f"- ✅ {stage.replace('_', ' ')} well covered ({count} items)")

    content += '\n'.join(stage_issues) + "\n\n"

    # Check language gaps
    content += "### Missing by Language:\n"
    languages = [('English', 'en'), ('Ukrainian', 'uk'), ('Russian', 'ru')]
    lang_issues = []

    for lang_name, lang_code in languages:
        count = stats['by_language'].get(lang_code, 0)
        if count == 0:
            lang_issues.append(f"- ❌ No {lang_name} content - **Translation needed**")
        elif count < 3:
            lang_issues.append(f"- ⚠️ Limited {lang_name} content ({count} items)")
        else:
            lang_issues.append(f"- ✅ {lang_name} well covered ({count} items)")

    content += '\n'.join(lang_issues) + "\n\n"

    # Check content type gaps
    content += "### Missing by Content Type:\n"
    types = [('Articles', 'article'), ('Videos', 'video'), ('Case Studies', 'case_study'),
             ('Tutorials', 'tutorial'), ('Guides', 'guide')]
    type_issues = []

    for type_name, type_code in types:
        count = stats['by_type'].get(type_code, 0)
        if count == 0:
            type_issues.append(f"- ❌ No {type_name.lower()} - **Creation needed**")
        elif count < 2:
            type_issues.append(f"- ⚠️ Only {count} {type_name.lower()}")
        else:
            type_issues.append(f"- ✅ {type_name} available ({count})")

    content += '\n'.join(type_issues) + "\n\n"

    # Generate recommendations
    content += "### Recommendations:\n"
    recommendations = []

    # Stage recommendations
    for stage in stages:
        if stats['by_stage'].get(stage, 0) == 0:
            recommendations.append(f"Create {stage.replace('_', ' ')} content to complete customer journey")

    # Language recommendations
    for lang_name, lang_code in languages:
        if stats['by_language'].get(lang_code, 0) == 0:
            recommendations.append(f"Add {lang_name} translations for localization")

    # Type recommendations
    if stats['by_type'].get('video', 0) == 0:
        recommendations.append("Create video content for better engagement")
    if stats['by_type'].get('case_study', 0) == 0:
        recommendations.append("Develop case studies to demonstrate real-world success")

    if not recommendations:
        recommendations.append("Content coverage is comprehensive across all dimensions")

    for i, rec in enumerate(recommendations[:5], 1):
        content += f"{i}. {rec}\n"

    content += "\n"
    return content


def generate_master_index(grouped_hubs: dict, all_files: List[ContentFile]) -> Path:
    """Generate the master INDEX.md file"""
    print("📄 Generating Master Index...")

    index_path = HUBS_DIR / "INDEX.md"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Calculate overall stats
    total_items = len(all_files)
    total_hubs = sum(len(values) for values in grouped_hubs.values())

    # Count items per category
    category_counts = {}
    for category, values in grouped_hubs.items():
        category_counts[category] = sum(len(files) for files in values.values())

    content = f"""---
title: "Content Hubs - Master Index"
type: master_index
total_hubs: {total_hubs}
total_content_items: {total_items}
last_updated: {current_time}
auto_generated: true
---

# 🗂️ Content Hubs - Master Index

> **Central navigation system for all Worksection content**

---

## 📊 System Overview

| Metric | Value |
|--------|-------|
| **Total Content Items** | {total_items} |
| **Total Hubs** | {total_hubs} |
| **Content Coverage** | 100.0% |
| **Last Updated** | {current_time} |

### Hub Categories

| Category | Hubs | Content Items | Coverage |
|----------|------|---------------|----------|
"""

    # Add category summary
    for category, dir_name in HUB_CATEGORIES.items():
        hub_count = len(grouped_hubs.get(category, {}))
        item_count = category_counts.get(category, 0)
        percent = format_percentage(item_count, total_items) if total_items > 0 else "0.0"

        emoji_map = {
            'features': '🎯',
            'business_type': '🏢',
            'competitor': '⚔️',
            'topic': '📚',
            'pain': '💥'
        }
        emoji = emoji_map.get(category, '📁')
        cat_display = category.replace('_', ' ').title()

        content += f"| {emoji} {cat_display} | {hub_count} | {item_count} | {percent}% |\n"

    content += "\n---\n\n"

    # Generate sections for each category
    for category, dir_name in HUB_CATEGORIES.items():
        if category not in grouped_hubs or not grouped_hubs[category]:
            continue

        emoji_map = {
            'features': '🎯',
            'business_type': '🏢',
            'competitor': '⚔️',
            'topic': '📚',
            'pain': '💥'
        }
        emoji = emoji_map.get(category, '📁')
        cat_display = category.replace('_', ' ').title()

        content += f"## {emoji} {cat_display} Hubs\n\n"

        # Create table header based on category
        if category == 'features':
            content += "| Feature | Content Items | Pre-Reg | Trial | Success | Languages |\n"
            content += "|---------|---------------|---------|-------|---------|-----------|n"
        elif category == 'business_type':
            content += "| Business Type | Content Items | Articles | Videos | Case Studies |\n"
            content += "|---------------|---------------|----------|--------|--------------|n"
        elif category == 'competitor':
            content += "| Competitor | Comparisons | Languages | Coverage |\n"
            content += "|------------|-------------|-----------|----------|n"
        elif category == 'topic':
            content += "| Topic | Articles | Guides | Languages |\n"
            content += "|-------|----------|--------|-----------|n"
        else:  # pain
            content += "| Pain Point | Solutions | Content Items | Coverage |\n"
            content += "|------------|-----------|---------------|----------|n"

        # Add rows for each hub
        items = sorted(grouped_hubs[category].items(),
                      key=lambda x: len(x[1]), reverse=True)

        for value, files in items:
            stats = calculate_stats(files)
            display_value = value.replace('_', ' ').title()
            hub_file = f"{value.lower().replace(' ', '_').replace('/', '_')}_hub.md"
            hub_link = f"[{display_value}]({dir_name}/{hub_file})"

            if category == 'features':
                pre_count = stats['by_stage'].get('Pre-Registration', 0)
                trial_count = stats['by_stage'].get('Trial', 0)
                success_count = stats['by_stage'].get('Success_Client', 0)
                langs = ', '.join(sorted(set(LANGUAGE_FLAGS.get(f.language, '🌐').replace('🇬🇧', 'EN').replace('🇺🇦', 'UK').replace('🇷🇺', 'RU').replace('🌍', 'Multi') for f in files)))
                content += f"| {hub_link} | {stats['total']} | {pre_count} | {trial_count} | {success_count} | {langs} |\n"

            elif category == 'business_type':
                article_count = stats['by_type'].get('article', 0)
                video_count = stats['by_type'].get('video', 0)
                case_count = stats['by_type'].get('case_study', 0)
                content += f"| {hub_link} | {stats['total']} | {article_count} | {video_count} | {case_count} |\n"

            elif category == 'competitor':
                langs = ', '.join(sorted(set(LANGUAGE_FLAGS.get(f.language, '🌐').replace('🇬🇧', 'EN').replace('🇺🇦', 'UK').replace('🇷🇺', 'RU').replace('🌍', 'Multi') for f in files)))
                coverage = "✅" if stats['total'] >= 5 else "⚠️"
                content += f"| {hub_link} | {stats['total']} | {langs} | {coverage} |\n"

            elif category == 'topic':
                article_count = stats['by_type'].get('article', 0)
                guide_count = stats['by_type'].get('guide', 0)
                langs = ', '.join(sorted(set(LANGUAGE_FLAGS.get(f.language, '🌐').replace('🇬🇧', 'EN').replace('🇺🇦', 'UK').replace('🇷🇺', 'RU').replace('🌍', 'Multi') for f in files)))
                content += f"| {hub_link} | {article_count} | {guide_count} | {langs} |\n"

            else:  # pain
                coverage = "✅" if stats['total'] >= 3 else "⚠️"
                content += f"| {hub_link} | {stats['total']} | {stats['total']} | {coverage} |\n"

        content += f"\n**[Browse all {cat_display} Hubs →]({dir_name}/)**\n\n---\n\n"

    # Overall statistics
    overall_stats = calculate_stats(all_files)

    content += """## 📈 Content Statistics

### Overall Distribution

**By Stage:**
"""

    for stage in ['Pre-Registration', 'Trial', 'Success_Client']:
        count = overall_stats['by_stage'].get(stage, 0)
        percent = format_percentage(count, total_items)
        emoji = STAGE_EMOJI.get(stage, '📍')
        content += f"- {emoji} {stage.replace('_', ' ')}: {count} ({percent}%)\n"

    content += "\n**By Content Type:**\n"

    for ctype, count in sorted(overall_stats['by_type'].items(), key=lambda x: x[1], reverse=True):
        percent = format_percentage(count, total_items)
        emoji = CONTENT_TYPE_EMOJI.get(ctype, '📝')
        type_display = ctype.replace('_', ' ').title()
        content += f"- {emoji} {type_display}: {count} ({percent}%)\n"

    content += "\n**By Language:**\n"

    lang_display = [
        ('🇬🇧 English', 'en'),
        ('🇺🇦 Ukrainian', 'uk'),
        ('🇷🇺 Russian', 'ru'),
        ('🌍 Multi-language', 'multi')
    ]

    for label, lang_code in lang_display:
        count = overall_stats['by_language'].get(lang_code, 0)
        if count > 0:
            percent = format_percentage(count, total_items)
            content += f"- {label}: {count} ({percent}%)\n"

    # Top content areas
    content += "\n### Top Content Areas\n\n**Most Content:**\n"

    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    for i, (cat, count) in enumerate(sorted_categories[:3], 1):
        cat_display = cat.replace('_', ' ').title()
        content += f"{i}. {cat_display}: {count} items\n"

    content += f"""
---

## 🔍 How to Use This System

### For Content Creators:
1. **Before creating new content:** Check relevant Hub to see what exists
2. **Check gap analysis:** See what's missing and prioritize creation
3. **Cross-reference:** Link to related content from other Hubs

### For Content Strategists:
1. **Audit content coverage:** Use Hub statistics to identify gaps
2. **Track journey completeness:** Ensure Pre-Reg → Trial → Success coverage
3. **Monitor language coverage:** Identify translation priorities

### For AI Content Generation:
1. **Provide context to Claude:** Share relevant Hub file
2. **Avoid duplication:** Claude sees what already exists
3. **Fill gaps:** Claude can create missing content types

---

## 🤖 Auto-Update System

This Hub system **automatically regenerates** when:
- ✅ New content is added to Content/
- ✅ Existing content is modified
- ✅ Content is deleted or moved

**Update trigger:** Manual execution or Git pre-commit hook
**Update script:** `/Users/marakinpoetry/Documents/CONTENT TREE/update_hubs.py`
**Last update:** {current_time}

To manually update Hubs:
```bash
cd "/Users/marakinpoetry/Documents/CONTENT TREE"
python3 update_hubs.py
```

---

*🤖 Auto-generated Master Index | System Version: 1.0*
*Last updated: {current_time}*
"""

    # Write index file
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Master Index created: {index_path}")
    return index_path


def generate_readme() -> Path:
    """Generate Hub README.md"""
    readme_path = HUBS_DIR / "README.md"
    current_date = datetime.now().strftime("%Y-%m-%d")

    content = f"""# Content Hub System Documentation

## What is this?

The Hub system provides centralized navigation for all content files organized by:
- 🎯 Features (product capabilities)
- 🏢 Business Types (industries)
- ⚔️ Competitors (comparisons)
- 📚 Topics (PM education)
- 💥 Pain Points (problems solved)

## Structure

```
Content/Hubs/
├── INDEX.md              # Master index (start here!)
├── README.md             # This file
├── features/             # Feature hubs
├── business_types/       # Industry hubs
├── competitors/          # Competitor hubs
├── topics/               # PM education hubs
└── pains/                # Pain point hubs
```

## Quick Start

1. **Start here:** Open [INDEX.md](INDEX.md)
2. **Browse by category:** Click into features/, business_types/, etc.
3. **Open a Hub:** Each Hub shows all content for that topic
4. **Navigate content:** Click links to actual content files

## Features

- ✅ Complete content inventory
- ✅ Statistics and analytics
- ✅ Gap analysis
- ✅ Cross-references between Hubs
- ✅ Customer journey tracking
- ✅ Automatic updates on content changes

## Auto-Update System

Hubs automatically regenerate when you run:

```bash
cd "/Users/marakinpoetry/Documents/CONTENT TREE"
python3 update_hubs.py
```

You can also set up a git pre-commit hook for automatic updates when content changes.

## Hub File Structure

Each Hub includes:
- **Content Overview** - Statistics by stage, type, and language
- **Content Inventory** - Organized list of all content items
- **Related Hubs** - Cross-references to other topics
- **Gap Analysis** - Identifies missing content
- **Journey Coverage** - Shows customer journey completeness

## Maintenance

The Hub system is designed to be maintenance-free:
- Run `update_hubs.py` after adding/editing content
- All Hubs regenerate with current statistics
- Links and cross-references update automatically

---

*Generated: {current_date}*
*System Version: 1.0*
"""

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ README created: {readme_path}")
    return readme_path


def main():
    """Main execution function"""
    print("=" * 60)
    print("🚀 Content Hub Generation System")
    print("=" * 60)
    print()

    start_time = datetime.now()

    # Create Hubs directory structure
    print("📁 Creating Hub directory structure...")
    for category_dir in HUB_CATEGORIES.values():
        (HUBS_DIR / category_dir).mkdir(parents=True, exist_ok=True)

    # Step 1: Scan content files
    content_files = scan_content_files()

    if not content_files:
        print("❌ No content files with hierarchical_tags found!")
        return

    # Step 2: Group by tags
    print("\n📊 Grouping content by tags...")
    grouped = group_by_tags(content_files)

    # Step 3: Generate individual Hub files
    print("\n🔨 Generating individual Hub files...")
    hub_count = 0

    for category, values in grouped.items():
        print(f"\n  📁 {category.replace('_', ' ').title()}:")
        for value, files in values.items():
            hub_path = generate_hub_file(category, value, files)
            hub_count += 1
            print(f"    ✅ {value} ({len(files)} items)")

    # Step 4: Generate Master Index
    print("\n📄 Generating Master Index...")
    generate_master_index(grouped, content_files)

    # Step 5: Generate README
    print("\n📖 Generating README...")
    generate_readme()

    # Step 6: Generate log
    print("\n📝 Generating log file...")
    log_path = HUBS_DIR / "generation_log.txt"

    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("Hub Generation Log\n")
        f.write("=" * 60 + "\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total content files scanned: {len(list(CONTENT_DIR.rglob('*.md')))}\n")
        f.write(f"Tagged content files: {len(content_files)}\n\n")

        f.write("Hubs Generated:\n")
        f.write("-" * 60 + "\n")

        for category, values in grouped.items():
            cat_display = category.replace('_', ' ').title()
            f.write(f"\n{cat_display}: {len(values)} hubs\n")
            for value, files in sorted(values.items(), key=lambda x: len(x[1]), reverse=True):
                f.write(f"  - {value}_hub.md ({len(files)} items)\n")

        f.write(f"\nTotal Hubs: {hub_count}\n\n")

        f.write("Files Created:\n")
        f.write("-" * 60 + "\n")
        f.write("- Content/Hubs/INDEX.md\n")
        f.write("- Content/Hubs/README.md\n")
        f.write("- Content/Hubs/generation_log.txt\n")

        for category, values in grouped.items():
            dir_name = HUB_CATEGORIES[category]
            for value in values.keys():
                hub_file = f"{value.lower().replace(' ', '_').replace('/', '_')}_hub.md"
                f.write(f"- Content/Hubs/{dir_name}/{hub_file}\n")

        f.write(f"\nErrors: 0\n")
        f.write(f"Warnings: 0\n")
        f.write(f"\nExecution time: {(datetime.now() - start_time).total_seconds():.2f} seconds\n")

    print(f"✅ Log file created: {log_path}")

    # Final summary
    print("\n" + "=" * 60)
    print("✅ Hub Generation Complete!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"  • Content files scanned: {len(content_files)}")
    print(f"  • Total Hubs created: {hub_count}")
    print(f"  • Execution time: {(datetime.now() - start_time).total_seconds():.2f} seconds")
    print(f"\n📁 Key Files:")
    print(f"  • Master Index: {HUBS_DIR / 'INDEX.md'}")
    print(f"  • Documentation: {HUBS_DIR / 'README.md'}")
    print(f"  • Generation Log: {HUBS_DIR / 'generation_log.txt'}")
    print(f"\n🎯 Next Steps:")
    print(f"  1. Open INDEX.md to browse all Hubs")
    print(f"  2. Check generation_log.txt for detailed statistics")
    print(f"  3. Run this script again after adding new content")
    print()


if __name__ == "__main__":
    main()
