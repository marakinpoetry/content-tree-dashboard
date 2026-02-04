"""
Normalization mappings for Content Tree database.
Maps folder names and file attributes to canonical DB values.
"""

# --- Products ---
PRODUCTS = ["WS 1.0", "WS 2.0", "WS 2.0 Release"]

# --- Stages ---
STAGES = ["Pre-Registration", "Trial", "Success_Client"]

# Stage name normalization (folder name → canonical)
STAGE_ALIASES = {
    "Pre-Registration": "Pre-Registration",
    "Pre-registration": "Pre-Registration",
    "Pre-registration 2": "Pre-Registration",
    "Pre-Registration 2": "Pre-Registration",
    "Trial": "Trial",
    "Trial 2": "Trial",
    "Trial 2 ": "Trial",
    "Success_Client": "Success_Client",
    "Success 2": "Success_Client",
}

# --- Categories ---
CATEGORIES = ["Features", "Business_Types", "Pains", "Competitors", "PM_Education"]

# Category name normalization (folder name → canonical)
CATEGORY_ALIASES = {
    "Features": "Features",
    "Business_Types": "Business_Types",
    "Business Type": "Business_Types",
    "Business_Type": "Business_Types",
    "Pains": "Pains",
    "Competitors": "Competitors",
    "PM_Education": "PM_Education",
}

# --- Topics by category ---
# Actual topics from Content/WS 1.0/ directory structure

TOPICS = {
    "Features": [
        "API",
        "Automation",
        "Brand_Ads",
        "Calendar",
        "Comments",
        "Custom_Fields",
        "Dark_Theme",
        "Dashboards",
        "File_Management",
        "Filters_Search",
        "Gantt_Chart",
        "Integrations",
        "Kanban",
        "Labels_Tags",
        "Migration",
        "Mobile_App",
        "Permissions",
        "Projects",
        "Reports",
        "Subtasks",
        "Task_Dependencies",
        "Tasks",
        "Teams",
        "Time_Material",
        "Time_Tracking",
        "User_Roles",
    ],
    "Business_Types": [
        "Agencies",
        "Architects",
        "Construction",
        "Consulting",
        "Education",
        "Enterprise",
        "Finance",
        "Government",
        "Healthcare",
        "Legal",
        "Manufacturing",
        "Media",
        "Non_Profits",
        "Other",
        "Retail",
        "Software",
        "Startups",
    ],
    "Competitors": [
        "Asana",
        "Basecamp",
        "Bitrix24",
        "ClickUp",
        "Jira",
        "Monday",
        "Notion",
        "Telegram",
        "Trello",
    ],
    "Pains": [
        "Chat_Overload",
        "File_Loss",
        "Missed_Deadlines",
        "No_Transparency",
        "Task_Chaos",
        "Too_Many_Tools",
    ],
    "PM_Education": [
        "Frameworks",
        "Methodologies",
        "Skills",
        "Strategy",
    ],
}

# --- Content Types ---
# 7 canonical content types
CONTENT_TYPES = [
    ("article", "Article"),
    ("landing", "Landing"),
    ("video", "Video"),
    ("static_ad", "Static Ad"),
    ("video_ad", "Video Ad"),
    ("smm", "SMM"),
    ("other", "Other"),
]

# Folder name → canonical content type
CONTENT_TYPE_ALIASES = {
    "articles": "article",
    "article": "article",
    "landings": "landing",
    "landing": "landing",
    "videos": "video",
    "video": "video",
    "static_ad": "static_ad",
    "static_ads": "static_ad",
    "video_ad": "video_ad",
    "video_ads": "video_ad",
    "smm": "smm",
    "ads": "ad",  # parent folder; resolved to static_ad/video_ad by subfolder
    # Special mappings
    "SEO_Outreach": "article",
    "seo_outreach": "article",
    "Case_Study": "article",
    "case_study": "article",
    "cases": "article",
    "Why_Worksection": "landing",
    "why_worksection": "landing",
    # Catch-all types
    "lead_magnets": "other",
    "guides": "other",
    "tutorials": "other",
    "pr&media": "other",
    "product hunt kit": "other",
    "webinars": "other",
    "influencer": "other",
    "other files": "other",
}

# File extension → content type (for files outside standard folders)
EXTENSION_CONTENT_TYPE = {
    ".md": None,  # determined by parent folder
    ".txt": None,
    ".png": "static_ad",
    ".jpg": "static_ad",
    ".jpeg": "static_ad",
    ".gif": "static_ad",
    ".webp": "static_ad",
    ".svg": "static_ad",
    ".mp4": "video",
    ".mov": "video",
    ".avi": "video",
    ".pdf": "other",
    ".pptx": "other",
    ".ppt": "other",
    ".csv": "other",
    ".xlsx": "other",
    ".xls": "other",
    ".docx": "other",
    ".doc": "other",
}

# --- Languages ---
LANGUAGES = [
    ("ua", "Українська", True),
    ("en", "English", True),
    ("ru", "Русский", False),
    ("pl", "Polski", False),
    ("pt", "Português", False),
    ("fr", "Français", False),
    ("it", "Italiano", False),
    ("ro", "Română", False),
    ("kz", "Қазақша", False),
]

# Filename suffix → language code
LANGUAGE_ALIASES = {
    "uk": "ua",
    "ua": "ua",
    "en": "en",
    "ru": "ru",
    "pl": "pl",
    "de": "de",
    "fr": "fr",
    "es": "es",
}

# --- Statuses ---
STATUSES = ["published", "draft", "idea", "review", "approved", "blocked"]

STATUS_ALIASES = {
    "published": "published",
    "active": "published",
    "draft": "draft",
    "idea": "idea",
    "brief": "idea",
    "review": "review",
    "approved": "approved",
    "blocked": "blocked",
}

# --- Priorities ---
# (stage, category, content_type, language, priority, label)
# NULL (None) means "any"
PRIORITY_RULES = [
    ("Trial", None, "article", "ua", 1, "Critical"),
    ("Trial", None, "landing", "ua", 1, "Critical"),
    ("Pre-Registration", "Features", "article", "ua", 2, "High"),
    (None, None, "article", "en", 2, "High"),
    (None, None, "landing", "ua", 2, "High"),
    (None, None, "video", "ua", 3, "Medium"),
    (None, None, "article", "ru", 3, "Medium"),
    (None, None, "landing", "en", 3, "Medium"),
    (None, None, "smm", None, 4, "Low"),
    (None, None, "static_ad", None, 4, "Low"),
    (None, None, "video_ad", None, 4, "Low"),
]

# --- Excluded directories ---
EXCLUDED_DIRS = {"Hubs", ".git", "__pycache__", ".DS_Store", ".claude", ".github", "node_modules"}


def display_name(topic_name: str) -> str:
    """Convert topic folder name to display name: 'Gantt_Chart' → 'Gantt Chart'."""
    return topic_name.replace("_", " ")
