# Dashboard та Auto-Sync система

Документація системи моніторингу прогресу Content Tree з автоматичною синхронізацією з Google Drive.

---

## Огляд системи

Dashboard — це веб-інтерфейс для моніторингу прогресу створення контенту. Показує:
- Загальну кількість файлів та покриття
- Розподіл по стадіях воронки (Pre-Registration, Trial, Success_Client, WS 2.0)
- Типи контенту (статті, відео, лендінги тощо)
- Мовне покриття
- Аналіз прогалин (gaps)

**Продакшн URL:** https://marakinpoetry.github.io/content-tree-dashboard/

---

## Архітектура

### Компоненти системи

```
┌─────────────────────────────────────────────────────────────────┐
│                        ЛОКАЛЬНІ МАШИНИ                         │
│  ┌─────────────┐                                               │
│  │ Google Drive│ ◄── Колеги додають контент                    │
│  │  Desktop    │                                               │
│  └──────┬──────┘                                               │
│         │ auto-sync                                            │
│         ▼                                                      │
│  ┌─────────────┐      ┌─────────────────┐                     │
│  │  Content/   │ ──── │ make dashboard  │ → localhost:8080    │
│  │   (папка)   │      │  (локальний)    │                     │
│  └─────────────┘      └─────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
         │
         │ Google Drive Cloud
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     GITHUB ACTIONS (кожні 3 години)             │
│                                                                 │
│  1. rclone sync wscontentdrive:Content ./Content                │
│                         │                                       │
│                         ▼                                       │
│  2. python scripts/generate_dashboard_data.py                   │
│                         │                                       │
│                         ▼                                       │
│  3. git push data.json                                          │
│                         │                                       │
└─────────────────────────┼───────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GITHUB PAGES (прод)                        │
│                                                                 │
│   https://marakinpoetry.github.io/content-tree-dashboard/       │
│                                                                 │
│   index.html ◄── fetch ── data.json                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Ключові файли

| Файл | Призначення |
|------|-------------|
| `Dashboard/index.html` | UI Dashboard (HTML + JS) |
| `scripts/generate_dashboard_data.py` | Генерація data.json |
| `.github/workflows/main.yml` | GitHub Action автосинку |
| `data.json` | Дані для Dashboard |

---

## Локальний запуск

### Швидкий старт

```bash
cd "/Users/marakinpoetry/Documents/CONTENT TREE"
make dashboard
```

### Що відбувається

1. Запускається `Dashboard/server.py`
2. Сервер слухає на порту 8080
3. Відкривається браузер з Dashboard

### Оновлення даних локально

```bash
# Згенерувати свіжий data.json
python scripts/generate_dashboard_data.py

# Оновити сторінку в браузері (F5)
```

### Зупинка

```bash
make dashboard-stop
# або
./Dashboard/stop_dashboard.sh
```

---

## Продакшн (GitHub Pages)

### URL

```
https://marakinpoetry.github.io/content-tree-dashboard/
```

### Як оновлюються дані

1. **GitHub Action** запускається кожні 3 години (cron: `0 */3 * * *`)
2. **rclone** синхронізує `Content/` з Google Drive
3. **generate_dashboard_data.py** сканує файли та генерує `data.json`
4. **git push** автоматично пушить зміни
5. **GitHub Pages** оновлює статичний сайт

### Кнопка "Оновити"

На продакшені кнопка "Оновити":
- Робить `fetch('data.json?t=' + Date.now())` — cache-busting
- Оновлює UI з новими даними
- **НЕ запускає** синхронізацію (дані оновлюються автоматично)

### Ручний запуск синхронізації

Якщо потрібно оновити дані терміново (не чекати 3 години):

1. Перейти на https://github.com/marakinpoetry/content-tree-dashboard
2. Actions → Sync Dashboard from Google Drive
3. Run workflow → Run workflow

---

## Налаштування автосинку

### Передумови

1. rclone встановлений та налаштований з Google Drive
2. Remote називається `wscontentdrive`
3. Доступ до GitHub репозиторію

### Крок 1: Перевірити rclone конфігурацію

```bash
# Перевірити що remote існує
rclone listremotes

# Має показати:
# wscontentdrive:

# Перевірити доступ
rclone lsd wscontentdrive:Content
```

### Крок 2: Отримати rclone.conf

```bash
cat ~/.config/rclone/rclone.conf
```

### Крок 3: Закодувати в base64

```bash
base64 -i ~/.config/rclone/rclone.conf
```

Скопіювати весь output (суцільний рядок без переносів).

### Крок 4: Додати секрет в GitHub

1. Перейти в GitHub репозиторій
2. Settings → Secrets and variables → Actions
3. New repository secret
4. Name: `RCLONE_CONFIG`
5. Secret: вставити base64 рядок
6. Add secret

### Верифікація

1. Actions → Sync Dashboard from Google Drive
2. Run workflow → Run workflow
3. Перевірити що job завершився успішно (зелена галочка)

---

## Технічні деталі

### generate_dashboard_data.py

**Розташування:** `/Users/marakinpoetry/scripts/generate_dashboard_data.py`

**Що робить:**
- Сканує `Content/` папку рекурсивно
- Підтримувані формати: `.md`, `.txt`, `.csv`, `.docx`
- Виключає: `Hubs/`, `.DS_Store`, `*.tmp`
- Визначає stage, section, content_type, language з шляху та файлу
- Генерує метрики та статистику

**Запуск:**
```bash
python scripts/generate_dashboard_data.py
```

**Output:**
```
Dashboard Data Generator
==================================================
Scanning content folder: /Users/marakinpoetry/Content
Found 600+ content files

Saved: /Users/marakinpoetry/data.json

Summary:
  Total files: 608
  Total folders: 245
  Fill rate: 67.3%
  Gaps found: 50

Done!
```

### GitHub Action workflow

**Файл:** `.github/workflows/main.yml`

```yaml
name: Sync Dashboard from Google Drive

on:
  schedule:
    - cron: '0 */3 * * *'  # Кожні 3 години
  workflow_dispatch:        # Ручний запуск

permissions:
  contents: write           # Дозвіл на push

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install pyyaml
      - uses: AnimMouse/setup-rclone@v1
        with:
          rclone_config: ${{ secrets.RCLONE_CONFIG }}
      - run: rclone sync wscontentdrive:Content ./Content --exclude ".DS_Store" --exclude "*.tmp" -v
      - run: python scripts/generate_dashboard_data.py
      - run: |
          git config user.name "GitHub Action"
          git config user.email "action@github.com"
          git add data.json
          git diff --staged --quiet || git commit -m "Auto-update"
          git push
```

### data.json структура

```json
{
  "metadata": {
    "last_update": "2026-01-30T12:00:00",
    "total_files": 608,
    "total_folders": 245,
    "fill_rate": 67.3
  },
  "by_stage": {
    "WS 1.0/Pre-Registration": 450,
    "WS 1.0/Trial": 80,
    "WS 1.0/Success_Client": 20,
    "WS 2.0 Release": 58
  },
  "by_content_type": {
    "Articles": 400,
    "Videos": 100,
    "Landings": 50,
    "Ads": 30,
    "SMM": 28
  },
  "by_language": {
    "Ukrainian": 250,
    "English": 200,
    "Russian": 100,
    "Polish": 58
  },
  "stages_detail": {
    "WS 1.0/Pre-Registration": {
      "total_files": 450,
      "by_section": {"Features": 150, "Business_Types": 120, ...},
      "folder_tree": {...},
      "recent_changes": [...]
    }
  },
  "gaps": [...],
  "search_index": [...]
}
```

---

## Troubleshooting

### Дані не оновлюються на проді

**Симптоми:** Dashboard показує застарілу дату last_update

**Рішення:**
1. Перевірити GitHub Actions:
   - https://github.com/marakinpoetry/content-tree-dashboard/actions
   - Подивитись чи останній run успішний
2. Перевірити логи якщо failed
3. Спробувати запустити вручну (Run workflow)

### GitHub Action failed: Permission denied

**Помилка:** `Permission to ... denied to github-actions[bot]`

**Рішення:** Додати в workflow:
```yaml
permissions:
  contents: write
```

### rclone: Command sync needs 2 arguments

**Причина:** Trailing spaces в YAML після `\`

**Рішення:** Писати rclone команду в один рядок:
```yaml
- run: rclone sync wscontentdrive:Content ./Content --exclude ".DS_Store" --exclude "*.tmp" -v
```

### Dashboard показує старі дані локально

**Рішення:**
```bash
# Перегенерувати data.json
python scripts/generate_dashboard_data.py

# Hard refresh браузера
# Mac: Cmd+Shift+R
# Windows: Ctrl+Shift+R
```

### RCLONE_CONFIG не працює

**Перевірка:**
1. Переконатись що base64 без переносів рядка
2. Remote має називатись `wscontentdrive`
3. Token не expired (перезапустити `rclone config` локально)

---

## Пов'язані документи

- [AUTOMATION.md](../docs/AUTOMATION.md) — загальна автоматизація
- [GOOGLE_DRIVE_SYNC.md](../docs/GOOGLE_DRIVE_SYNC.md) — ручний sync з Google Drive
- [OVERVIEW.md](../docs/OVERVIEW.md) — огляд проєкту

---

**Останнє оновлення:** 2026-01-30
