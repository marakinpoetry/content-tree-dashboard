# Content Tree — Worksection Marketing Content System

## Project Overview

Content Tree is an AI-powered content management system for **Worksection** (Ukrainian project management SaaS).

**Goal:** 960 content units across 4 customer journey stages
**Current Progress:** 448/960 (46.7%)
**Languages:** Ukrainian, English, Russian, Polish (primary)

---

## Three Core Systems

### 1. Content Generation System

**Location:** `Content/`

**Stages (customer journey):**
| Stage | Purpose | Path |
|-------|---------|------|
| Pre-Registration | Awareness & Consideration | `Content/WS 1.0/Pre-Registration/` |
| Trial | Activation & Onboarding | `Content/WS 1.0/Trial/` |
| Success_Client | Retention & Upsell | `Content/WS 1.0/Success_Client/` |
| WS 2.0 Release | New release content | `Content/WS 2.0 Release/` |

**Categories within each stage:**
- `Features/` — 8 product features (Gantt, Time Tracking, Kanban, etc.)
- `Business_Types/` — 9+ industries (Agencies, Construction, IT, etc.)
- `Competitors/` — 7+ competitors (Trello, Asana, Monday, etc.)
- `Pains/` — 6 pain points addressed
- `PM_Education/` — Educational PM content

**Content types:**
- `/articles/` — Blog posts (1800-3500 words)
- `/videos/` — Video scripts
- `/landings/` — Landing pages
- `/smm/` — Social media posts
- `/ads/` — Static ads, video ads, lead magnets
- `/guides/` — Step-by-step tutorials

**Command:** `/generate` — interactive content generation

---

### 2. SEO Agent

**Location:** `SEO AGENT/`

**Purpose:** Generate SEO-optimized, humanized content (<25% AI detection score)

**Key files:**
- `WS semantic full.csv` — Main keyword database (2.3MB, search volumes included)
- `semantic core worksection - competitors.csv` — Competitor keywords
- `USAGE.md` — Complete usage guide with 100+ command examples
- `agent guidelines/` — Templates, humanization rules, TT briefs

**Workflow:**
1. Parse topic, content type, business segment, language
2. Search semantic CSVs for relevant keywords
3. Generate SEO brief or optimized content
4. Apply humanization rules
5. Save with hierarchical tags for auto-hub updates

---

### 3. Dashboard

**Location:** `Dashboard/`

**Launch:**
```bash
make dashboard
# or
./Dashboard/start_dashboard.sh
```

**Access:** http://localhost:8080

**Features:**
- Real-time content metrics
- Progress tracking (960-file goal)
- Breakdown by stage, type, language, status
- Growth trends (files added per week/month)
- Visual charts (Chart.js)

**Stop:** `make dashboard-stop` or `./Dashboard/stop_dashboard.sh`

---

## Key Commands

| Command | Action |
|---------|--------|
| `/generate` | Generate new content (interactive or quick mode) |
| `make update` | Update 59 navigation hubs |
| `make dashboard` | Start analytics dashboard |
| `make dashboard-stop` | Stop dashboard |
| `make publish` | Publish to WordPress CMS |
| `make all` | Update hubs + publish |

---

## Project Structure

```
Content/              # Content library (4 stages, 448+ files)
├── WS 1.0/           # Worksection 1.0 content
│   ├── Pre-Registration/ # Awareness content
│   ├── Trial/            # Onboarding content
│   └── Success_Client/   # Retention content
├── WS 2.0 Release/   # New release content
└── Hubs/             # 59 auto-generated navigation hubs

Dashboard/            # Analytics & monitoring
├── server.py         # Python HTTP server
├── index.html        # Web UI
└── data.json         # Auto-generated metrics

SEO AGENT/            # SEO optimization
├── *.csv             # Semantic keyword databases
├── USAGE.md          # Usage guide
├── agent guidelines/ # Templates & rules
└── generated/        # Output directory

WS KNOWLEDGE BASE/    # Source data for content
├── marketing/        # Marketing materials
├── product/          # Product docs
├── sales/            # Sales materials
└── support/          # FAQ & support

docs/                 # Documentation
├── OVERVIEW.md
├── STRUCTURE.md
├── TONE_OF_VOICE.md  # Brand voice guidelines
├── CONTENT_TEMPLATES.md
├── PROMPTS.md        # AI prompts library
└── SEO_AGENT_GUIDE.md

.claude/
└── commands/
    └── generate.md   # /generate command definition
```

---

## Content Generation Rules

### Hierarchical Tags (required in frontmatter)
Every content file must have:
```yaml
---
hierarchical_tags:
  - stage: Pre-Registration
    category: Features
    subcategory: Gantt Chart
    content_type: article
    language: uk
---
```

### Tone of Voice
- Professional but approachable
- Focus on practical value
- See `docs/TONE_OF_VOICE.md` for full guidelines

### SEO Requirements
- Use keywords from `SEO AGENT/*.csv`
- Target AI detection score: <25%
- Apply humanization rules from `SEO AGENT/agent guidelines/naturalize-content-prompt.md`

### Languages
| Code | Language |
|------|----------|
| uk | Ukrainian |
| en | English |
| ru | Russian |
| pl | Polish |

---

## Important Reference Files

| File | Purpose |
|------|---------|
| `CONTENT_TREE_PROJECT_PLAN.md` | Full project blueprint (142KB) |
| `ONBOARDING.md` | Beginner's guide |
| `docs/PROMPTS.md` | AI prompts library |
| `docs/CONTENT_TEMPLATES.md` | Content templates |
| `docs/TONE_OF_VOICE.md` | Brand voice |
| `SEO AGENT/USAGE.md` | SEO agent guide |

---

## Quick Start

1. **Generate content:** `/generate`
2. **Check progress:** `make dashboard`
3. **Update hubs after adding content:** `make update`
4. **Publish:** `make publish`

---

## Notes for Claude

- Always check `WS KNOWLEDGE BASE/` for accurate product information
- Use semantic CSVs in `SEO AGENT/` for keyword research
- Follow templates in `docs/CONTENT_TEMPLATES.md`
- Apply humanization rules to avoid AI detection
- Update hubs after creating new content files
