# Content Tree - Автоматизація та Скрипти

## Зміст
- [Огляд автоматизації](#огляд-автоматизації)
- [update_hubs.py — Генератор хабів](#update_hubspy--генератор-хабів)
- [Dashboard — Моніторинг прогресу](#dashboard--моніторинг-прогресу)
- [Інші скрипти](#інші-скрипти)
- [Workflows та інтеграції](#workflows-та-інтеграції)
- [Troubleshooting](#troubleshooting)

---

## Огляд автоматизації

Content Tree має кілька автоматизованих систем для ефективного управління контентом.

### Ключові компоненти автоматизації

**1. Hub Navigation Generator (update_hubs.py)**
- Автоматично генерує 59 Hub files
- Сканує всі .md файли та витягує теги
- Створює gap analysis
- Генерує INDEX.md

**2. Dashboard System**
- Web-інтерфейс для моніторингу
- Real-time статистика
- Візуалізація прогресу
- Auto-refresh функціонал

**3. Content Scripts**
- Migration scripts
- Tagging automation
- Analysis tools
- Reporting generators

### Переваги автоматизації

✅ **Швидкість:** Hub generation за 1 секунду
✅ **Точність:** Автоматичний підрахунок статистики
✅ **Консистентність:** Однакова структура всіх хабів
✅ **Gap Analysis:** Автоматичне виявлення відсутнього контенту
✅ **Масштабованість:** Працює з 448+ файлами легко

---

## update_hubs.py — Генератор хабів

**Розташування:** `/Users/marakinpoetry/Documents/CONTENT TREE/update_hubs.py`

**Призначення:** Автоматична генерація всієї Hub навігаційної системи.

### Що робить скрипт

1. **Сканує контент:**
   - Знаходить всі .md файли в `/Content/`
   - Витягує YAML frontmatter
   - Парсить hierarchical_tags

2. **Групує за тегами:**
   - По primary.category (features, business_type, etc.)
   - По primary.value (конкретна тема)

3. **Генерує хаби:**
   - 59 Hub files (по 1 для кожної унікальної теми)
   - Розподілені по 5 категоріях папок

4. **Створює статистику:**
   - Stage coverage
   - Content type distribution
   - Language distribution
   - Gap analysis

5. **Генерує INDEX.md:**
   - Master navigation file
   - Overall statistics
   - Links до всіх 59 хабів

6. **Логує процес:**
   - Створює generation_log.txt
   - Detailed report про що згенеровано

### Встановлення

**Вимоги:**
- Python 3.6 або вище
- PyYAML library

**Установка PyYAML:**
```bash
pip3 install pyyaml
```

**Перевірка встановлення:**
```bash
python3 -c "import yaml; print('PyYAML installed:', yaml.__version__)"
```

### Використання

**Базове використання:**
```bash
cd "/Users/marakinpoetry/Documents/CONTENT TREE"
python3 update_hubs.py
```

**Очікуваний вивід:**
```
Content Tree Hub Generator
==========================

Scanning content files...
Found 448 markdown files with hierarchical tags

Grouping by tags...
  Features: 12 unique values
  Business Types: 13 unique values
  Competitors: 13 unique values
  Topics: 19 unique values
  Pains: 2 unique values

Generating hub files...
  ✓ Generated 12 feature hubs
  ✓ Generated 13 business_type hubs
  ✓ Generated 13 competitor hubs
  ✓ Generated 19 topic hubs
  ✓ Generated 2 pain hubs

Generating master INDEX.md...
  ✓ INDEX.md created

Writing generation log...
  ✓ Log saved to generation_log.txt

Summary:
========
Total hubs generated: 59
Total content items: 448
Execution time: 0.8 seconds

Done! Check Content/Hubs/ for results.
```

### Коли запускати

**Обов'язково після:**
- ✅ Додавання нового контентного файлу
- ✅ Редагування hierarchical_tags
- ✅ Видалення файлів
- ✅ Зміни в структурі категорій

**Рекомендовано:**
- 📅 Щодня якщо активно додається контент
- 📅 Перед важливими презентаціями/звітами
- 📅 Після bulk content imports

**Можна не запускати після:**
- Редагування тексту контенту (без зміни тегів)
- Виправлення typos
- Оновлення metadata крім hierarchical_tags

### Структура коду

**Основні функції:**

#### 1. `extract_frontmatter(file_path)`
```python
# Витягує YAML frontmatter з markdown файлу
# Returns: dict з метаданими або None
```

#### 2. `scan_content_files(content_dir)`
```python
# Сканує всі .md файли в Content/
# Витягує теги з кожного
# Returns: list of ContentFile objects
```

#### 3. `group_by_tags(content_files)`
```python
# Групує файли за primary.category та value
# Returns: dict з групами
```

#### 4. `generate_hub_file(category, value, files, output_dir)`
```python
# Генерує один Hub file
# Включає:
#   - Overview statistics
#   - Content inventory по стейджах
#   - Gap analysis
#   - Related hubs
```

#### 5. `generate_master_index(groups, output_path)`
```python
# Створює INDEX.md
# Включає:
#   - System overview
#   - Total stats
#   - Links до всіх хабів
```

#### 6. `analyze_gaps(files, category, value)`
```python
# Аналізує що відсутнє:
#   - Missing stages
#   - Missing languages
#   - Missing content types
# Returns: recommendations
```

### Output файли

**Hubs:**
```
Content/Hubs/
├── features/
│   ├── projects_hub.md
│   ├── gantt_chart_hub.md
│   └── ... (12 total)
├── business_types/
│   ├── agencies_hub.md
│   ├── construction_hub.md
│   └── ... (13 total)
├── competitors/
│   ├── trello_hub.md
│   └── ... (13 total)
├── topics/
│   ├── strategy_strategic_planning_hub.md
│   └── ... (19 total)
├── pains/
│   ├── task_chaos_hub.md
│   └── ... (2 total)
└── INDEX.md
```

**Logs:**
```
generation_log.txt — детальний лог процесу генерації
```

### Налаштування

**Змінити output директорію:**
```python
# У update_hubs.py знайдіть:
HUBS_DIR = "Content/Hubs"

# Змініть на:
HUBS_DIR = "your/custom/path"
```

**Додати нову категорію:**
```python
# У VALID_CATEGORIES додайте:
VALID_CATEGORIES = [
    "features",
    "business_type",
    "competitor",
    "topic",
    "pain",
    "your_new_category"  # додати тут
]
```

**Змінити шаблон Hub:**
```python
# Функція generate_hub_file() містить template
# Редагуйте markdown template за потреби
```

---

## Dashboard — Моніторинг прогресу

> **Повна документація:** [Dashboard/README.md](../Dashboard/README.md) — включає автосинк з Google Drive, налаштування GitHub Actions, troubleshooting.

**Розташування:** `/Users/marakinpoetry/Documents/CONTENT TREE/Dashboard/`

**Призначення:** Інтерактивний web-інтерфейс для моніторингу прогресу Content Tree.

### Компоненти Dashboard

```
Dashboard/
├── server.py              # Python HTTP server
├── update_dashboard.py    # Data generator script
├── data.json             # Dashboard data (auto-generated)
├── index.html            # Frontend UI
├── styles.css            # Styling
├── script.js             # Interactive JavaScript
├── start_dashboard.sh    # Quick start script
├── stop_dashboard.sh     # Stop server script
└── refresh.sh            # Manual data refresh
```

### Запуск Dashboard

**Швидкий запуск (рекомендовано):**
```bash
cd "/Users/marakinpoetry/Documents/CONTENT TREE"
./Dashboard/start_dashboard.sh
```

**Що відбувається:**
1. Оновлює data.json з поточної статистики
2. Запускає HTTP server на порт 8080
3. Відкриває браузер автоматично

**Відкрити в браузері:**
```
http://localhost:8080
```

**Зупинити Dashboard:**
```bash
./Dashboard/stop_dashboard.sh
```

### Ручний запуск (покроково)

**Крок 1: Оновити дані**
```bash
cd "/Users/marakinpoetry/Documents/CONTENT TREE/Dashboard"
python3 update_dashboard.py
```

**Крок 2: Запустити server**
```bash
python3 server.py
```

**Крок 3: Відкрити браузер**
```
http://localhost:8080
```

### Що показує Dashboard

**1. Overall Progress**
- Total content items: 448 / 960 (46.7%)
- Progress bar з візуалізацією
- До скількох потрібно ще створити

**2. Stage Breakdown**
- Pre-Registration: 406 (90.6%)
- Trial: 41 (9.2%)
- Success_Client: 1 (0.2%)
- Pie chart або bar chart

**3. Category Distribution**
- Business_Types: 152 (33.9%)
- Topics: 132 (29.5%)
- Features: 108 (24.1%)
- Competitors: 50 (11.2%)
- Pains: 6 (1.3%)

**4. Content Type Analysis**
- Articles: 351 (78.3%)
- Videos: 71 (15.8%)
- Ads: 21 (4.7%)
- Landings: 3 (0.7%)
- Guides: 2 (0.4%)

**5. Language Coverage**
- English: 173 (38.6%)
- Ukrainian: 160 (35.7%)
- Multi: 66 (14.7%)
- Russian: 49 (10.9%)

**6. Top Hubs**
- List топ-10 хабів за кількістю контенту
- Links до Hub files

**7. Critical Gaps**
- Success_Client стейдж (критичний!)
- Pain Points (критичний!)
- Landing pages (потребує уваги)
- Case studies (потребує уваги)

**8. Recent Activity**
- Останні додані файли
- Timestamp останнього оновлення

### Auto-refresh

Dashboard може автоматично оновлювати дані:

**Налаштування в script.js:**
```javascript
// Auto-refresh кожні 30 секунд
setInterval(() => {
    fetchDashboardData();
}, 30000);
```

**Вимкнути auto-refresh:**
```javascript
// Закоментувати в script.js:
// setInterval(() => { ... }, 30000);
```

### Оновлення даних вручну

**Якщо Dashboard вже запущений:**
```bash
# В іншому terminal вікні:
cd "/Users/marakinpoetry/Documents/CONTENT TREE/Dashboard"
python3 update_dashboard.py

# Оновіть сторінку в браузері (F5)
```

**Або використати refresh script:**
```bash
./Dashboard/refresh.sh
```

### data.json структура

```json
{
  "overall": {
    "total_items": 448,
    "target": 960,
    "progress_percent": 46.7
  },
  "by_stage": {
    "Pre-Registration": 406,
    "Trial": 41,
    "Success_Client": 1
  },
  "by_category": {
    "business_type": 152,
    "topic": 132,
    "features": 108,
    "competitor": 50,
    "pain": 6
  },
  "by_content_type": {
    "article": 351,
    "video": 71,
    "ad": 21,
    "landing": 3,
    "guide": 2
  },
  "by_language": {
    "en": 173,
    "uk": 160,
    "multi": 66,
    "ru": 49
  },
  "top_hubs": [
    {
      "name": "agencies",
      "category": "business_type",
      "count": 70
    },
    ...
  ],
  "critical_gaps": [
    {
      "type": "stage",
      "name": "Success_Client",
      "current": 1,
      "severity": "critical"
    },
    ...
  ],
  "last_updated": "2024-10-31T14:30:00Z"
}
```

### Кастомізація Dashboard

**Змінити порт:**
```python
# У server.py:
PORT = 8080  # Змініть на інший порт
```

**Додати нову метрику:**
```python
# У update_dashboard.py:
# Додайте до data dictionary:
data["your_metric"] = calculate_your_metric()
```

```javascript
// У script.js:
// Додайте відображення:
document.getElementById('your-metric').textContent = data.your_metric;
```

**Змінити стилі:**
```css
/* У styles.css */
/* Налаштуйте кольори, fonts, layout */
```

---

## Інші скрипти

### consolidate_article_folders.py

**Призначення:** Консолідація article контенту з різних папок.

**Використання:**
```bash
python3 consolidate_article_folders.py
```

**Що робить:**
- Знаходить всі /articles/ та /articles/ папки
- Об'єднує в єдину структуру
- Уникає дублікатів

---

### content_gap_analysis.py

**Призначення:** Детальний аналіз гепів у контенті.

**Використання:**
```bash
python3 content_gap_analysis.py
```

**Output:**
- Список відсутніх стейджів по кожній темі
- Відсутні мови
- Відсутні типи контенту
- Пріоритизовані рекомендації

**Вивід:**
```
Content Gap Analysis Report
===========================

CRITICAL GAPS:
--------------
1. Success_Client stage: Missing 99% content
   - Priority: CRITICAL
   - Recommendation: Create 100+ items

2. Pain Points: 4 of 6 pains have NO content
   - Missing: Missed_Deadlines, File_Loss, Chat_Overload, Too_Many_Tools
   - Priority: CRITICAL

HIGH PRIORITY GAPS:
-------------------
1. Trial stage: Only 9.2% coverage
   - Recommendation: Create onboarding content

2. Landing pages: Only 3 items total
   - Recommendation: Create landing for top 15 features

[Детальний breakdown...]
```

---

### migrate_blog_articles_final.py

**Призначення:** Міграція blog статей з MySQL database до Content Tree.

**Використання:**
```bash
python3 migrate_blog_articles_final.py
```

**Що робить:**
- Читає статті з database export
- Конвертує до markdown
- Додає hierarchical_tags
- Зберігає в правильну структуру папок

**Note:** Використовувався для initial setup, тепер в основному історичний.

---

## Workflows та інтеграції

### Workflow 1: Додавання нового контенту

```bash
# 1. Створити контент з правильними тегами
# (використати промпти з PROMPTS.md)

# 2. Зберегти файл у відповідну папку
# Content/[Stage]/[Category]/[Topic]/[Type]/filename.md

# 3. Оновити Hub navigation
cd "/Users/marakinpoetry/Documents/CONTENT TREE"
python3 update_hubs.py

# 4. Перевірити що файл з'явився в Hub
open "Content/Hubs/[category]/[topic]_hub.md"

# 5. Оновити Dashboard (якщо запущений)
cd Dashboard
python3 update_dashboard.py

# 6. Перевірити Dashboard
open "http://localhost:8080"
```

---

### Workflow 2: Bulk content import

```bash
# 1. Підготувати всі файли з тегами

# 2. Скопіювати в правильні папки
# (можна використати rsync або cp)

# 3. Запустити tagging verification
python3 verify_tags.py  # якщо є такий скрипт

# 4. Оновити всю навігацію
python3 update_hubs.py

# 5. Перевірити логи
cat generation_log.txt

# 6. Оновити Dashboard
cd Dashboard
python3 update_dashboard.py

# 7. Review в Dashboard
```

---

### Workflow 3: Щоденний моніторинг

```bash
# Ранковий check:

# 1. Запустити Dashboard
./Dashboard/start_dashboard.sh

# 2. Переглянути прогрес та гепи

# 3. Визначити пріоритети на день
# (використати Critical Gaps секцію)

# 4. Створити контент для закриття гепів
# (використати PROMPTS.md)

# 5. Вкінці дня оновити все
python3 update_hubs.py
cd Dashboard && python3 update_dashboard.py

# 6. Перевірити що metrics покращились
```

---

### Workflow 4: Тижневий звіт

```bash
# 1. Оновити всі дані
python3 update_hubs.py
cd Dashboard && python3 update_dashboard.py

# 2. Зробити screenshot Dashboard
# (Overall progress, Stage breakdown)

# 3. Експортувати ключові метрики:
cat generation_log.txt | grep "Total"
# Total hubs: 59
# Total content: 448

# 4. Check top growth areas
# Порівняти з попереднім тижнем

# 5. Ідентифікувати проблеми
python3 content_gap_analysis.py > weekly_gaps.txt

# 6. Підготувати звіт
```

---

## Troubleshooting

### Проблема: update_hubs.py не запускається

**Симптом:**
```
ModuleNotFoundError: No module named 'yaml'
```

**Рішення:**
```bash
pip3 install pyyaml
# Або якщо потрібен sudo:
sudo pip3 install pyyaml
```

---

### Проблема: Dashboard не відкривається

**Симптом:**
```
Address already in use: Port 8080
```

**Рішення 1: Зупинити існуючий процес**
```bash
./Dashboard/stop_dashboard.sh
# Потім запустити знову
./Dashboard/start_dashboard.sh
```

**Рішення 2: Використати інший порт**
```python
# Редагувати Dashboard/server.py:
PORT = 8081  # Змінити на вільний порт
```

---

### Проблема: Файл не з'являється в Hub

**Можливі причини:**

**1. Відсутні hierarchical_tags**
```bash
# Перевірити файл:
head -20 "path/to/file.md"

# Має бути YAML frontmatter з hierarchical_tags
```

**Рішення:** Додати теги (див. TAGS_AND_NAVIGATION.md)

**2. Невірний category або value**
```yaml
# WRONG:
category: feature  # має бути features (plural)
value: TimeTracking  # має бути time_tracking (snake_case)

# CORRECT:
category: features
value: time_tracking
```

**Рішення:** Виправити теги, перезапустити `update_hubs.py`

**3. Файл поза Content/ директорією**
```bash
# update_hubs.py сканує тільки:
/Content/WS 1.0/Pre-Registration/
/Content/WS 1.0/Trial/
/Content/WS 1.0/Success_Client/
/Content/WS 2.0 Release/
```

**Рішення:** Перемістити файл в правильну папку

---

### Проблема: Dashboard показує старі дані

**Симптом:** Додали контент, але Dashboard не оновився

**Рішення:**
```bash
# 1. Оновити data.json
cd Dashboard
python3 update_dashboard.py

# 2. Hard refresh браузера
# Chrome/Firefox: Ctrl+Shift+R (Windows) або Cmd+Shift+R (Mac)
# Safari: Cmd+Option+R

# 3. Якщо не допомогло - перезапустити server
cd ..
./Dashboard/stop_dashboard.sh
./Dashboard/start_dashboard.sh
```

---

### Проблема: Генерація хабів дуже повільна

**Симптом:** update_hubs.py працює більше 5 секунд

**Можливі причини:**

**1. Дуже багато файлів**
```bash
# Перевірити кількість:
find Content -name "*.md" | wc -l
```

Якщо >1000 файлів, це нормально що повільніше.

**2. Великі файли**
```bash
# Знайти великі файли:
find Content -name "*.md" -size +1M
```

**Рішення:** Оптимізувати або розбити великі файли

**3. Disk I/O issues**

**Рішення:** Закрити інші програми, перевірити disk space

---

### Проблема: Gap Analysis неточний

**Симптом:** Hub показує "missing stage" але контент існує

**Причина:** Невірний stage в тегах

**Перевірка:**
```bash
# Знайти файли певного топіку:
grep -r "value: time_tracking" Content/ | grep "stage: Trial"
```

**Рішення:** Виправити stage в hierarchical_tags, перегенерувати хаби

---

## Автоматизація в майбутньому

### Можливості для розширення

**1. CI/CD Integration**
```yaml
# GitHub Actions example
name: Update Hubs
on:
  push:
    paths:
      - 'Content/**/*.md'
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run update_hubs.py
        run: python3 update_hubs.py
      - name: Commit changes
        run: |
          git add Content/Hubs/
          git commit -m "Auto-update hubs"
          git push
```

**2. Slack Integration**
```python
# Повідомлення в Slack після генерації
import requests

def notify_slack(stats):
    webhook_url = "YOUR_WEBHOOK_URL"
    message = f"Hubs updated: {stats['total']} items"
    requests.post(webhook_url, json={"text": message})
```

**3. Scheduled Updates**
```bash
# Cron job для автоматичного оновлення
# crontab -e
0 */6 * * * cd /path/to/CONTENT\ TREE && python3 update_hubs.py
```

**4. Content Quality Checks**
```python
# Автоматична перевірка якості контенту:
# - Spelling/grammar
# - SEO optimization
# - Proper tags
# - Required sections
```

---

## Best Practices

### Автоматизація

**✅ DO:**
- Запускайте update_hubs.py після кожної зміни тегів
- Тримайте Dashboard запущеним під час активної роботи
- Regularly check generation_log.txt для помилок
- Commit hub files до git разом з контентом

**❌ DON'T:**
- Не редагуйте Hub files вручну (вони перезапишуться)
- Не запускайте кілька інстансів update_hubs.py одночасно
- Не ігноруйте warnings в логах

### Моніторинг

**Щоденно:**
- Перевіряти Dashboard для overall progress
- Переглядати Critical Gaps
- Планувати контент based on gaps

**Щотижня:**
- Запускати content_gap_analysis.py
- Порівнювати прогрес з попереднім тижнем
- Оновлювати пріоритети

**Щомісяця:**
- Повний audit всіх хабів
- Перевірка consistency тегів
- Review automation scripts для оптимізації

---

## Висновки

Автоматизація в Content Tree дозволяє:

✅ Швидко генерувати навігацію (1 сек для 448 файлів)
✅ Моніторити прогрес в real-time
✅ Автоматично виявляти гепи
✅ Масштабувати до 1000+ файлів
✅ Підтримувати consistency

### Наступні кроки

**Почніть використовувати:**
1. Запустіть Dashboard: `./Dashboard/start_dashboard.sh`
2. Додайте новий контент
3. Оновіть хаби: `python3 update_hubs.py`
4. Перевірте результат в Dashboard

**Вивчіть інші документи:**
- [OVERVIEW.md](./OVERVIEW.md) — загальний огляд проєкту
- [PROMPTS.md](./PROMPTS.md) — генерація контенту
- [TAGS_AND_NAVIGATION.md](./TAGS_AND_NAVIGATION.md) — система тегів

---

**Останнє оновлення:** 2025-10-31
**Версія:** 1.0
