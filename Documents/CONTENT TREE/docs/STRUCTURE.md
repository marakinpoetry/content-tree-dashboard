# Content Tree - Структура Папок

## Зміст
- [Загальна структура](#загальна-структура)
- [Content — Основна бібліотека](#content--основна-бібліотека)
- [WS Knowledge Base](#ws-knowledge-base)
- [Hubs — Система навігації](#hubs--система-навігації)
- [Dashboard](#dashboard)
- [Топ-10 хабів за контентом](#топ-10-хабів-за-контентом)
- [Швидкий пошук](#швидкий-пошук)

---

## Загальна структура

```
/Users/marakinpoetry/Documents/CONTENT TREE/
│
├── 📚 Content/                          # Основна бібліотека контенту (525 файлів)
│   ├── WS 1.0/                         # Worksection 1.0 контент
│   │   ├── Pre-Registration/           # Стейдж 1: Залучення (406 файлів)
│   │   ├── Trial/                      # Стейдж 2: Активація (41 файл)
│   │   └── Success_Client/             # Стейдж 3: Утримання (1 файл)
│   ├── WS 2.0 Release/                 # Спеціальний: запуск WS 2.0
│   └── Hubs/                           # Автоматична навігація (59 хабів)
│
├── 📖 WS KNOWLEDGE BASE/                # База знань для створення контенту
│   ├── _landing_essentials/            # Критичні дані
│   ├── marketing/                      # Маркетингові матеріали
│   ├── product/                        # Продуктова документація
│   ├── competitors/                    # Аналіз конкурентів
│   ├── support/                        # FAQ та підтримка
│   ├── success/                        # Customer success
│   ├── sales/                          # Sales матеріали
│   └── external/                       # Зовнішні ресурси
│
├── 📊 Dashboard/                        # Моніторинг прогресу
│   ├── server.py
│   ├── update_dashboard.py
│   ├── data.json
│   ├── start_dashboard.sh
│   └── stop_dashboard.sh
│
├── 📄 docs/                             # Документація проєкту
│   ├── OVERVIEW.md
│   ├── STAGES.md
│   ├── STRUCTURE.md (цей файл)
│   ├── TAGS_AND_NAVIGATION.md
│   ├── PROMPTS.md
│   └── AUTOMATION.md
│
├── 🤖 Scripts/                          # Автоматизація
│   ├── update_hubs.py                  # Генератор хабів
│   ├── consolidate_article_folders.py
│   ├── content_gap_analysis.py
│   ├── migrate_blog_articles_final.py
│   └── [інші скрипти]
│
└── 📋 Logs & Reports/                   # Логи та звіти
    ├── tagging_summary.txt
    ├── tagging_log.txt
    ├── generation_log.txt
    ├── COMPLETION_REPORT.md
    └── [інші звіти]
```

---

## Content — Основна бібліотека

**Шлях:** `/Users/marakinpoetry/Documents/CONTENT TREE/Content/`

**Загальна статистика:** 525 файлів (448 з тегами)

### Pre-Registration/

**Шлях:** `Content/WS 1.0/Pre-Registration/`
**Файлів:** 406 (90.6%)

Найбільший стейдж, розділений на 5 категорій:

#### 1. Competitors/ (50 файлів)

```
WS 1.0/Pre-Registration/Competitors/
│
├── Asana/
│   ├── ads/
│   │   ├── static_ad/          # Статичні рекламні банери
│   │   ├── video_ad/           # Відео-реклама
│   │   └── lead_magnet/        # Лід-магніти (чек-листи, шаблони)
│   ├── articles/               # Порівняльні статті
│   ├── SEO_Outreach/          # SEO-статті
│   ├── videos/                # Відео огляди
│   ├── landings/              # Лендінги
│   └── smm/                   # SMM контент
│
├── Basecamp/
├── Bitrix24/
├── ClickUp/
├── Jira/
├── Monday/
├── Notion/
├── Telegram/
├── Trello/
├── Wrike/
├── Smartsheet/
└── [інші конкуренти]
```

**Приклади шляхів:**
- `/Content/WS 1.0/Pre-Registration/Competitors/Asana/articles/Worksection_vs_Asana_Comprehensive_Comparison_en.md`
- `/Content/WS 1.0/Pre-Registration/Competitors/Trello/SEO_Outreach/Best_Trello_Alternatives_for_Project_Management_en.md`

**Топ-3 конкурента за контентом:**
1. Trello (11 items)
2. Telegram (8 items)
3. Asana (5 items)

---

#### 2. Features/ (108 файлів)

```
WS 1.0/Pre-Registration/Features/
│
├── Projects/                   # 37 items — найбільший feature hub!
│   ├── Ads/
│   │   ├── static_ad/
│   │   ├── video_ad/
│   │   └── lead_magnet/
│   ├── articles/
│   ├── SEO_Outreach/
│   ├── videos/
│   ├── landings/
│   └── smm/
│
├── Gantt_Chart/               # 16 items
├── Kanban/                    # 13 items
├── Time_Tracking/             # 13 items
├── Tasks/                     # 11 items
├── Integrations/              # 12 items
│
├── Reports/
├── Teams/
├── Comments/
├── Dashboards/
├── Calendar/
├── File_Management/
├── User_Roles/
├── Permissions/
├── Custom_Fields/
├── Labels_Tags/
├── Filters_Search/
├── Task_Dependencies/
├── Subtasks/
│
├── Automation/                # 4 items
├── Migration/                 # 3 items
├── Mobile_App/                # 1 item — гэп!
├── Dark_Theme/
└── API/
```

**Приклади шляхів:**
- `/Content/WS 1.0/Pre-Registration/Features/Projects/articles/Comprehensive_Guide_to_Project_Management_with_Worksection_en.md`
- `/Content/WS 1.0/Pre-Registration/Features/Gantt_Chart/SEO_Outreach/Best_Gantt_Chart_Software_2024_en.md`
- `/Content/WS 1.0/Pre-Registration/Features/Time_Tracking/ads/video_ad/Time_Tracking_Feature_Ad_Script_ua.md`

**Топ-5 features за контентом:**
1. Projects (37 items)
2. Gantt_Chart (16 items)
3. Kanban (13 items)
4. Time_Tracking (13 items)
5. Integrations (12 items)

---

#### 3. Business_Types/ (152 файли — найбільша категорія!)

```
WS 1.0/Pre-Registration/Business_Types/
│
├── Agencies/                   # 70 items — НАЙБІЛЬШИЙ ХАБ!
│   ├── ads/
│   │   ├── static_ad/
│   │   │   ├── creative_1_facebook_ad_ua.md
│   │   │   ├── creative_2_instagram_ad_en.md
│   │   │   └── ...
│   │   ├── video_ad/
│   │   │   ├── video_script_youtube_en.md
│   │   │   └── ...
│   │   └── lead_magnet/
│   │       ├── agency_checklist_en.md
│   │       └── ...
│   │
│   ├── Why_Worksection/       # Value proposition для агенцій
│   │   ├── Why_Agencies_Choose_Worksection_en.md
│   │   ├── Worksection_for_Marketing_Agencies_ua.md
│   │   └── ...
│   │
│   ├── Case_Study/            # Success stories
│   │   ├── Agency_Success_Story_RomanUA_ua.md
│   │   ├── Digital_Agency_Case_Study_en.md
│   │   └── ...
│   │
│   ├── articles/              # Довгі статті
│   ├── landings/              # Лендінги для агенцій
│   ├── videos/                # Відео контент
│   └── smm/                   # Social media
│
├── Construction/              # 17 items
├── Software/                  # 16 items
├── Government/                # 12 items
├── Retail/                    # 9 items
│
├── Manufacturing/
├── Education/
├── Healthcare/
├── Finance/
├── Legal/
├── Media/
├── Startups/
├── Consulting/
├── Non_Profits/
├── Enterprise/
└── Other/
```

**Приклади шляхів:**
- `/Content/WS 1.0/Pre-Registration/Business_Types/Agencies/Why_Worksection/Why_Agencies_Choose_Worksection_en.md`
- `/Content/WS 1.0/Pre-Registration/Business_Types/Construction/Case_Study/Construction_Company_Success_Story_ua.md`
- `/Content/WS 1.0/Pre-Registration/Business_Types/Software/ads/static_ad/Software_Development_Teams_Facebook_Ad_en.md`

**Топ-5 індустрій за контентом:**
1. Agencies (70 items) — 46% від усіх Business_Types!
2. Construction (17 items)
3. Software (16 items)
4. Government (12 items)
5. Retail (9 items)

---

#### 4. PM_Education/ (132 файли — 2-га за розміром)

```
WS 1.0/Pre-Registration/PM_Education/
│
├── Methodologies/
│   ├── Agile/                 # 35 items — найбільший топік!
│   │   └── articles/
│   │       ├── Comprehensive_Guide_to_Lean_vs_Agile_Methodologies_en.md
│   │       ├── What_is_Agile_Project_Management_ua.md
│   │       └── ...
│   ├── Lean/
│   ├── Scrum/
│   ├── Waterfall/
│   └── Kanban_Method/
│
├── Skills/
│   ├── Management_Skills/     # 15 items
│   │   └── articles/
│   ├── Team_Leadership/
│   ├── Remote_Hybrid_Work/    # 3 items
│   └── Organizational_Structure/  # 3 items
│
├── Frameworks/
│   ├── OKR_KPI/              # 11 items
│   │   └── articles/
│   │       ├── OKR_vs_KPI_Complete_Comparison_Guide_en.md
│   │       └── ...
│   ├── SMART_Goals/          # 6 items
│   ├── RACI/                 # 2 items
│   ├── RAID/                 # 2 items
│   └── Eisenhower_Matrix/    # 1 item — гэп!
│
└── Strategy/
    ├── Strategic_Planning/    # 43 items — НАЙБІЛЬШИЙ ТОПІК!
    │   └── articles/
    │       ├── Complete_Guide_to_Strategic_Planning_en.md
    │       ├── Strategic_Planning_Process_Step_by_Step_ua.md
    │       └── ...
    ├── Goal_Setting/
    └── Decision_Making/       # 2 items
```

**Приклади шляхів:**
- `/Content/WS 1.0/Pre-Registration/PM_Education/Strategy/Strategic_Planning/articles/Complete_Guide_to_Strategic_Planning_en.md`
- `/Content/WS 1.0/Pre-Registration/PM_Education/Methodologies/Agile/articles/Comprehensive_Guide_to_Lean_vs_Agile_Methodologies_en.md`
- `/Content/WS 1.0/Pre-Registration/PM_Education/Frameworks/OKR_KPI/articles/OKR_vs_KPI_Complete_Comparison_Guide_en.md`

**Топ-5 топіків за контентом:**
1. Strategic_Planning (43 items) — найбільший топік в усій системі!
2. Agile (35 items)
3. Management_Skills (15 items)
4. OKR_KPI (11 items)
5. SMART_Goals (6 items)

---

#### 5. Pains/ (6 файлів — критичний гэп!)

```
WS 1.0/Pre-Registration/Pains/
│
├── Task_Chaos/                # 5 items
│   ├── ads/
│   │   └── static_ad/
│   │       └── creative_ad_facebook_ads_business_type_ua.md
│   └── articles/
│       └── How_to_Eliminate_Task_Chaos_with_Worksection_en.md
│
├── No_Transparency/           # 1 item
│   └── articles/
│       └── How_to_Improve_Project_Transparency_en.md
│
├── Missed_Deadlines/          # 0 items — ВІДСУТНІЙ!
├── File_Loss/                 # 0 items — ВІДСУТНІЙ!
├── Chat_Overload/             # 0 items — ВІДСУТНІЙ!
└── Too_Many_Tools/            # 0 items — ВІДСУТНІЙ!
```

**Приклади шляхів:**
- `/Content/WS 1.0/Pre-Registration/Pains/Task_Chaos/ads/static_ad/creative_ad_facebook_ads_business_type_ua.md`
- `/Content/WS 1.0/Pre-Registration/Pains/No_Transparency/articles/How_to_Improve_Project_Transparency_en.md`

**Статус:** Критичний гэп — 4 з 6 болей повністю відсутні!

---

### Trial/

**Шлях:** `Content/WS 1.0/Trial/`
**Файлів:** 41 (9.2%)

```
WS 1.0/Trial/
│
├── Features/                  # Навчання функціям
│   ├── Projects/
│   │   └── videos/
│   │       └── 20250331_What_is_Worksection_Full_Walkthrough__Key_Features_transcript.md
│   │
│   ├── Mobile_App/
│   │   └── videos/
│   │       └── worksection_app_how_to_use_tutorial_transcripts.md
│   │
│   ├── Time_Tracking/
│   ├── Gantt_Chart/
│   ├── Kanban/
│   └── [інші features]
│
└── Business_Types/            # Індустрія-специфічні гайди
    ├── Agencies/
    │   └── Case_Study/
    ├── Construction/
    ├── Software/
    └── [інші індустрії]
```

**Приклади шляхів:**
- `/Content/Trial/Features/Projects/videos/20250331_What_is_Worksection_Full_Walkthrough__Key_Features_transcript.md`
- `/Content/Trial/Features/Mobile_App/videos/worksection_app_how_to_use_tutorial_transcripts.md`

**Характеристика:** Переважно video transcripts (61% контенту)

---

### Success_Client/

**Шлях:** `Content/WS 1.0/Success_Client/`
**Файлів:** 1 (0.2%) — критичний гэп!

```
WS 1.0/Success_Client/
│
├── articles/                  # (планова структура)
├── Features/                  # Advanced tutorials
└── Business_Types/            # Customer success stories
```

**Статус:** Практично порожній стейдж, потребує негайного заповнення!

---

### WS 2.0 Release/

**Шлях:** `Content/WS 2.0 Release/`
**Файлів:** Спеціальна категорія

```
WS 2.0 Release/
│
├── articles/                  # Blog posts про WS 2.0
│   ├── Whats_New_in_Worksection_2.0_en.md
│   ├── WS_1.0_vs_2.0_Comparison_Table_ua.md
│   ├── New_Dashboards_Feature_Deep_Dive_en.md
│   └── ...
│
├── video/                     # Video контент
│   ├── WS_2.0_Product_Demo_transcript.md
│   ├── Feature_Highlights_Video_Script_en.md
│   └── ...
│
└── smm/                       # Social media
    ├── Launch_Announcement_Posts_ua.md
    ├── Feature_Teasers_series_en.md
    └── ...
```

**Призначення:** Time-sensitive контент для product launch

---

### Hubs/

**Шлях:** `Content/Hubs/`
**Файлів:** 59 Hub files + INDEX.md

Детальніше в розділі [Hubs — Система навігації](#hubs--система-навігації)

---

## WS Knowledge Base

**Шлях:** `/Users/marakinpoetry/Documents/CONTENT TREE/WS KNOWLEDGE BASE/`

База знань для референсу при створенні нового контенту.

### Структура

```
WS KNOWLEDGE BASE/
│
├── 🔥 _landing_essentials/        # КРИТИЧНО ВАЖЛИВА ПАПКА!
│   ├── pain_points.md            # Болі з 4,014 звернень
│   ├── success_stories.md        # 12+ case studies з метриками
│   ├── objections_responses.md   # Відповіді на 117 demo заперечень
│   ├── client_profiles.md        # 5 детальних ICP
│   └── README.md                 # Документація
│
├── marketing/
│   ├── Content/                  # Існуючий маркетинговий контент
│   ├── Testimonials/             # 90+ testimonials (UA/RU/EN)
│   ├── Advertising/              # Рекламні кампанії
│   ├── Analytics/                # Маркетингова аналітика
│   ├── Lead_generation/          # Лід-ген матеріали
│   └── research/                 # Ринкові дослідження
│
├── product/
│   ├── Worksection_2.0/         # WS 2.0 документація
│   │   ├── Product_docs/
│   │   ├── Features/
│   │   ├── Marketing_materials/
│   │   ├── FAQ_structure/
│   │   ├── Hub_page_content/
│   │   └── Time_tracking_landing/
│   └── [інша продуктова документація]
│
├── competitors/                  # Конкурентний аналіз
│   ├── Competitor_comparison_data.md
│   ├── Market_positioning.md
│   └── Feature_comparison_tables.xlsx
│
├── support/
│   ├── FAQ_Organized/           # 12 категорій FAQ
│   │   ├── account_management/
│   │   ├── api_integration/
│   │   ├── file_management/
│   │   ├── migration/
│   │   ├── mobile/
│   │   ├── notifications/
│   │   ├── project_management/
│   │   ├── reporting/
│   │   ├── settings/
│   │   ├── team_collaboration/
│   │   ├── time_tracking/
│   │   └── troubleshooting/
│   │
│   └── FAQ_WS2/                 # FAQ для WS 2.0
│
├── success/                     # Customer success data
│   ├── Customer_case_studies/
│   ├── ROI_calculations/
│   └── Success_metrics/
│
├── sales/                       # Sales матеріали
│   ├── Sales_decks/
│   ├── Demo_scripts/
│   ├── Pricing_comparisons/
│   └── Objection_handling/
│
└── external/                    # Зовнішні ресурси
    ├── Industry_reports/
    ├── PM_trends/
    └── Research_papers/
```

### Ключові файли в _landing_essentials/

#### pain_points.md

**Зміст:**
- Топ-20 болей клієнтів
- Джерело: 4,014 support conversations
- Frequency data
- Цитати від реальних користувачів
- Impact metrics

**Використання:** Для створення pain-focused контенту та ads

---

#### success_stories.md

**Зміст:**
- 12+ детальних case studies
- Метрики успіху:
  - % підвищення продуктивності
  - Економія часу (години/тиждень)
  - ROI ($saved or earned)
  - Кількість проєктів/користувачів
- До і після порівняння
- Цитати від клієнтів

**Використання:** Для Success_Client контенту та social proof

---

#### objections_responses.md

**Зміст:**
- Топ-50 заперечень з 117 demo calls
- Перевірені відповіді
- Success rate кожної відповіді
- Context коли використовувати

**Використання:** Для landing pages, sales content, FAQ

---

#### client_profiles.md

**Зміст:**
- 5 детальних Ideal Customer Profiles:
  1. Digital/Marketing Agency (15-50 співробітників)
  2. Software Development Company (20-100 developers)
  3. Construction Firm (30-200 співробітників)
  4. Government Organization (100-500 співробітників)
  5. Enterprise (500+ співробітників)
- Для кожного ICP:
  - Demographics
  - Pain points
  - Goals
  - Decision-making process
  - Budget
  - Success criteria

**Використання:** Для таргетованого контенту за індустріями

---

### Використання Knowledge Base

**При створенні нового контенту:**

1. **Статті** → використати product/ та marketing/Content/
2. **Ads** → використати pain_points.md та objections_responses.md
3. **Landing pages** → використати всі файли з _landing_essentials/
4. **Case studies** → використати success_stories.md
5. **FAQ** → використати support/FAQ_Organized/
6. **Competitor content** → використати competitors/

**Ключове правило:** Завжди перевіряти Knowledge Base перед створенням контенту!

---

## Hubs — Система навігації

**Шлях:** `Content/Hubs/`
**Файлів:** 59 Hub files + 1 INDEX.md

### Структура Hubs

```
Hubs/
│
├── INDEX.md                   # Master навігація по всіх хабах
│
├── features/                  # 12 хабів
│   ├── projects_hub.md       # 37 items — найбільший feature
│   ├── gantt_chart_hub.md    # 16 items
│   ├── kanban_hub.md         # 13 items
│   ├── time_tracking_hub.md  # 13 items
│   ├── integrations_hub.md   # 12 items
│   ├── tasks_hub.md
│   ├── automation_hub.md
│   ├── migration_hub.md
│   └── [інші features]
│
├── business_types/            # 13 хабів
│   ├── agencies_hub.md       # 70 items — НАЙБІЛЬШИЙ ХАБ!
│   ├── construction_hub.md   # 17 items
│   ├── software_hub.md       # 16 items
│   ├── government_hub.md     # 12 items
│   ├── retail_hub.md         # 9 items
│   └── [інші індустрії]
│
├── competitors/               # 13 хабів
│   ├── trello_hub.md         # 11 items
│   ├── telegram_hub.md       # 8 items
│   ├── asana_hub.md          # 5 items
│   └── [інші конкуренти]
│
├── topics/                    # 19 хабів
│   ├── strategy_strategic_planning_hub.md    # 43 items — найбільший топік!
│   ├── methodologies_agile_hub.md            # 35 items
│   ├── skills_management_skills_hub.md       # 15 items
│   ├── frameworks_okr_kpi_hub.md             # 11 items
│   └── [інші топіки]
│
└── pains/                     # 2 хаби
    ├── task_chaos_hub.md     # 5 items
    └── no_transparency_hub.md # 1 item
```

### Що містить кожен Hub

Кожен Hub file автоматично генерується та містить:

1. **Overview статистика**
   - Total items
   - Breakdown by stage
   - Breakdown by content type
   - Breakdown by language

2. **Content inventory**
   - Організовано по стейджах
   - Прямі посилання на файли
   - Індикатори мови

3. **Related hubs**
   - Cross-references
   - Content overlap analysis

4. **Gap analysis**
   - Missing stages
   - Missing languages
   - Missing content types
   - Recommendations

5. **Journey coverage score**
   - Completeness по стейджах
   - Status indicators

### INDEX.md

**Шлях:** `Content/Hubs/INDEX.md`

Master файл навігації:

**Зміст:**
- System overview
- Total statistics
- All 59 hubs organized by category
- Quick navigation links
- How to use instructions
- Update information

**Ключові метрики в INDEX:**
- Total Content Items: 448
- Total Hubs: 59
- Content Coverage: 100%
- Hub Categories: 5

Детальніше про Hubs в [TAGS_AND_NAVIGATION.md](./TAGS_AND_NAVIGATION.md)

---

## Dashboard

**Шлях:** `/Users/marakinpoetry/Documents/CONTENT TREE/Dashboard/`

### Структура

```
Dashboard/
│
├── server.py                  # HTTP server (port 8080)
├── update_dashboard.py        # Scan content + generate data.json
├── data.json                  # Dashboard data (auto-generated)
│
├── index.html                 # Dashboard UI
├── styles.css                 # Стилі
├── script.js                  # Interactive features
│
├── start_dashboard.sh         # Швидкий запуск
├── stop_dashboard.sh          # Зупинка server
└── refresh.sh                 # Manual update
```

### Використання

**Запустити Dashboard:**
```bash
cd "/Users/marakinpoetry/Documents/CONTENT TREE"
./Dashboard/start_dashboard.sh
```

**Відкрити в браузері:**
```
http://localhost:8080
```

**Зупинити Dashboard:**
```bash
./Dashboard/stop_dashboard.sh
```

### Що показує Dashboard

- 📊 Загальний прогрес (448 / 960 = 46.7%)
- 📈 Breakdown по стейджах
- 📂 Breakdown по категоріях
- 🌍 Breakdown по мовах
- 📝 Breakdown по типах контенту
- 🎯 Gap visualization
- 🔄 Auto-refresh кожні 30 секунд

Детальніше в [AUTOMATION.md](./AUTOMATION.md)

---

## Топ-10 хабів за контентом

### 1. Agencies (Business Type) — 70 items

**Шлях:** `Content/Hubs/business_types/agencies_hub.md`

**Найбільший хаб в усій системі!**

**Breakdown:**
- Pre-Registration: 70 items
- Trial: 0
- Success_Client: 0

**Content types:**
- Articles: 55
- Videos: 10
- Ads: 5

**Чому такий великий:** Agencies — ключова аудиторія Worksection

---

### 2. Strategic Planning (Topic) — 43 items

**Шлях:** `Content/Hubs/topics/strategy_strategic_planning_hub.md`

**Найбільший освітній топік!**

**Breakdown:**
- Pre-Registration: 43 items
- Всі article content type

**Чому такий великий:** Thought leadership стратегія

---

### 3. Projects (Feature) — 37 items

**Шлях:** `Content/Hubs/features/projects_hub.md`

**Найбільший feature hub!**

**Breakdown:**
- Pre-Registration: 35
- Trial: 2

**Content types:**
- Articles: 28
- Videos: 6
- Ads: 3

**Чому такий великий:** Projects — core feature Worksection

---

### 4. Agile (Topic) — 35 items

**Шлях:** `Content/Hubs/topics/methodologies_agile_hub.md`

**Breakdown:**
- Pre-Registration: 35
- Всі articles

---

### 5. Construction (Business Type) — 17 items

**Шлях:** `Content/Hubs/business_types/construction_hub.md`

---

### 6. Software (Business Type) — 16 items

**Шлях:** `Content/Hubs/business_types/software_hub.md`

---

### 7. Gantt Chart (Feature) — 16 items

**Шлях:** `Content/Hubs/features/gantt_chart_hub.md`

---

### 8. Management Skills (Topic) — 15 items

**Шлях:** `Content/Hubs/topics/skills_management_skills_hub.md`

---

### 9. Kanban (Feature) — 13 items

**Шлях:** `Content/Hubs/features/kanban_hub.md`

---

### 10. Time Tracking (Feature) — 13 items

**Шлях:** `Content/Hubs/features/time_tracking_hub.md`

---

## Швидкий пошук

### За категорією

**Features:**
```
/Content/WS 1.0/Pre-Registration/Features/[Feature_Name]/
/Content/Hubs/features/[feature_name]_hub.md
```

**Business Types:**
```
/Content/WS 1.0/Pre-Registration/Business_Types/[Industry_Name]/
/Content/Hubs/business_types/[industry_name]_hub.md
```

**Competitors:**
```
/Content/WS 1.0/Pre-Registration/Competitors/[Competitor_Name]/
/Content/Hubs/competitors/[competitor_name]_hub.md
```

**Topics (PM Education):**
```
/Content/WS 1.0/Pre-Registration/PM_Education/[Category]/[Topic_Name]/
/Content/Hubs/topics/[category]_[topic_name]_hub.md
```

**Pains:**
```
/Content/WS 1.0/Pre-Registration/Pains/[Pain_Name]/
/Content/Hubs/pains/[pain_name]_hub.md
```

### За стейджом

**Pre-Registration:**
```
/Content/WS 1.0/Pre-Registration/
```

**Trial:**
```
/Content/WS 1.0/Trial/
```

**Success_Client:**
```
/Content/WS 1.0/Success_Client/
```

### За типом контенту

**Articles:**
```
/Content/[Stage]/[Category]/[Topic]/articles/
/Content/[Stage]/[Category]/[Topic]/articles/
```

**Videos:**
```
/Content/[Stage]/[Category]/[Topic]/videos/
```

**Ads:**
```
/Content/[Stage]/[Category]/[Topic]/ads/
  ├── static_ad/
  ├── video_ad/
  └── lead_magnet/
```

**Landings:**
```
/Content/[Stage]/[Category]/[Topic]/landings/
/Content/[Stage]/[Category]/[Topic]/landings/
```

**SEO Content:**
```
/Content/WS 1.0/Pre-Registration/[Category]/[Topic]/SEO_Outreach/
```

### За мовою

Використовуйте команди:

```bash
# Знайти всі українські статті
find Content -name "*.md" -exec grep -l "language: uk" {} \;

# Знайти всі англійські статті
find Content -name "*.md" -exec grep -l "language: en" {} \;

# Знайти всі російські статті
find Content -name "*.md" -exec grep -l "language: ru" {} \;
```

Або використовуйте Hub navigation з фільтром по мовах.

---

## Умовні позначення в структурі

**📚 Content** — Основна бібліотека контенту
**📖 Knowledge Base** — Референсні матеріали
**🗺️ Hubs** — Автоматична навігація
**📊 Dashboard** — Моніторинг та аналітика
**🤖 Scripts** — Автоматизація
**📄 Docs** — Документація проєкту
**📋 Logs** — Логи та звіти

**✅ Сильно** — Добре покриття контентом
**⚠️ Потребує розширення** — Недостатньо контенту
**❌ Критичний гэп** — Майже відсутній контент

---

## Наступні кроки

**Вивчити систему тегів:**
→ Читайте [TAGS_AND_NAVIGATION.md](./TAGS_AND_NAVIGATION.md)

**Навчитися генерувати контент:**
→ Читайте [PROMPTS.md](./PROMPTS.md)

**Автоматизувати процеси:**
→ Читайте [AUTOMATION.md](./AUTOMATION.md)

**Зрозуміти стейджі:**
→ Читайте [STAGES.md](./STAGES.md)

---

**Останнє оновлення:** 2025-10-31
**Версія:** 1.0
