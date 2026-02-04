# SEO Agent Guide

Онбординг для SEO-спеціалістів по роботі з контент-агентом Worksection.

---

## Що таке SEO Agent?

AI-агент на базі Claude для автоматичної генерації SEO-оптимізованого контенту. Поєднує:

- **Семантичне ядро** (2.3MB CSV з ключовими словами)
- **Парсинг топ-10 Google** (аналіз конкурентів)
- **Knowledge Base Worksection** (ICP, болі, кейси)
- **Гуманізацію тексту** (AI detection <25%)

---

## Команди та режими

### Основна команда генерації

```bash
/generate [функція] [тип_бізнесу] [стейдж] "типи_контенту"
```

**Приклади:**
```bash
/generate діаграма_ганта агенції trial "стаття"
/generate time_tracking іт_компанії pre-registration "стаття,лендінг"
/generate kanban стартапи trial "креатив"
```

### SEO-режим (з семантикою)

```bash
/generate --seo monday alternative for small teams
```

Активує:
- Пошук по семантичному ядру
- Вибір primary/secondary keywords
- Keyword density 1-2%
- Гуманізацію тексту

### SEO Brief (тільки ТЗ)

```bash
/generate --seo-brief best task management software 2025
```

Генерує тільки технічне завдання:
- Keyword research
- Структура H1-H3
- Рекомендації по довжині
- Meta title/description

Контент генерується ПІСЛЯ затвердження brief.

### Ручні ключові слова

```bash
/generate --seo landing page for gantt charts --keywords="gantt chart software,project timeline tool"
```

Пропускає пошук по CSV, використовує вказані keywords.

### Інтерактивний режим

```bash
/generate
```

Агент питає параметри покроково через AskUserQuestion.

---

## Етапи роботи агента

### ЕТАП 1: SEO-аналіз топ-10 видачі

**Що відбувається:**

#### 1.1 Формування пошукового запиту

Автоматично з параметрів:
```
gantt_chart + agencies + trial → "діаграма Ганта для агенцій управління проектами"
```

#### 1.2 WebSearch (Google US)

```
WebSearch(query: "діаграма Ганта для агенцій")
```

**Обмеження:** Google US, не .ua

#### 1.3 WebFetch топ-10 сторінок

Для кожного URL витягує:
- H1 заголовок
- Всі H2 та H3
- Кількість слів
- Списки, таблиці, FAQ, відео
- CTA

#### 1.4 Формування SEO Brief

```
=== SEO АНАЛІЗ ТОП-10 ===

ПОШУКОВИЙ ЗАПИТ: "діаграма Ганта для агенцій"

СЕРЕДНЯ ДОВЖИНА: 2,400 слів (від 1,800 до 3,200)

ТИПОВІ H2 ЗАГОЛОВКИ:
1. "Що таке діаграма Ганта" - 9/10 сторінок
2. "Як створити діаграму Ганта" - 8/10 сторінок
3. "Переваги використання" - 7/10 сторінок

ОБОВ'ЯЗКОВІ ЕЛЕМЕНТИ:
- ✅ Списки (10/10)
- ✅ Зображення (9/10)
- ✅ FAQ секція (6/10)
- ❌ Відео (2/10)

РЕКОМЕНДАЦІЇ:
1. Мінімальна довжина: 2,400 слів
2. Обов'язкові секції: Що таке, Як створити, Переваги
3. Додати FAQ для featured snippets
```

---

### ЕТАП 2: Keyword Research (семантичне ядро)

**Джерела даних:**

| Файл | Що містить | Розмір |
|------|------------|--------|
| `WS semantic full.csv` | Повна база keywords | 2.3 MB |
| `semantic core - addition.csv` | Додаткові keywords | - |
| `semantic core - competitors.csv` | Конкурентні терміни | - |
| `semantic core - global (ua).csv` | Українські keywords | - |

**Шлях:** `/SEO AGENT/core semantic/`

**Що витягає агент:**

```
PRIMARY KEYWORD:
- Keyword: "monday alternative"
- Search Volume: 1,200/month
- Difficulty: Medium
- Intent: Commercial

SECONDARY KEYWORDS (5-10):
1. "monday pricing alternative" - 480/month
2. "cheap monday alternative" - 320/month
3. "monday competitor" - 290/month

LSI TERMS:
- project management tool
- task management software
- team collaboration
```

---

### ЕТАП 3: Knowledge Base (внутрішня семантика)

**Джерела:**

| Файл | Що містить | Як використовується |
|------|------------|---------------------|
| `client_profiles.md` | ICP, персони, ARPU | Таргетування аудиторії |
| `pain_points.md` | Болі з % частотою | Релевантні проблеми |
| `success_stories.md` | Кейси з метриками | Соціальні докази |
| `objections_responses.md` | Заперечення | Робота з сумнівами |

**Шлях:** `/WS KNOWLEDGE BASE/_landing_essentials/`

**Приклад даних:**

```
ICP "Операційний інтегратор" (agencies):
- Розмір: 30-100 людей
- ARPU: $89/місяць
- Retention: 94%
- Болі: хаос у задачах, пропущені дедлайни

Pain "Project Visibility Crisis":
- Частота: 22% з 4,014 звернень
- Impact: "Агенції втрачають 15% прибутку"

Success Story:
- Компанія: Marketing Office
- Результат: 50 клієнтів, 0 missed deadlines
```

---

### ЕТАП 4: Гуманізація (обов'язково для SEO mode)

**Джерело правил:** `/SEO AGENT/agent guidelines/naturalize-content-prompt.md`

**Ціль:** AI detection score <25%

**Техніки:**

| Що робити | Приклад |
|-----------|---------|
| Скорочення | it's, don't, we're, you'll |
| Різна довжина речень | 5-25 слів, mix коротких і довгих |
| Розмовні фрази | "Here's the thing", "Honestly", "Let's be real" |
| Питання до читача | "Ever felt this way?", "Sound familiar?" |
| Особисті займенники | we, you, our, your |

**Заборонено:**

- ❌ "In today's fast-paced world"
- ❌ "It's important to note that"
- ❌ "Furthermore", "Moreover"
- ❌ Повторювані AI-патерни

---

### ЕТАП 5: Генерація контенту

**Формула:**

```
Контент = SEO Brief (топ-10) + Keywords (CSV) + KB (дані) + Гуманізація
```

**При генерації агент:**

- Довжина ≥ середньої конкурентів
- Включає всі типові H2 з топ-10
- Keyword density 1-2%
- Додає TL;DR та FAQ (AI Overview optimization)
- Вставляє реальні метрики з KB
- Застосовує гуманізацію

---

## Типи контенту та шаблони

| Тип | Коли використовувати | Слів | Ціль |
|-----|---------------------|------|------|
| **SEO Brief** | `--seo-brief` flag | 500-800 | Keyword research, структура |
| **Blog Article** | Освітній контент | 1,800-3,200 | Traffic + engagement |
| **Comparison** | vs конкуренти | 2,000-3,500 | Conversion + traffic |
| **Landing Page** | Feature pages | 1,200-2,000 | Conversion |
| **Complete Guide** | Ultimate guides | 2,500-4,000 | Authority + traffic |
| **Case Study** | Success stories | 1,000-1,800 | Trust + conversion |

**Шаблони:** `/SEO AGENT/knowledge_base/seo_content_templates.md`

---

## Структура вихідного файлу

### YAML Frontmatter

```yaml
---
title: "Article Title"
date: 2024-11-20
author: "Content Team"

hierarchical_tags:
  primary:
    category: features  # або business_type, competitor
    value: gantt_chart
  content_attributes:
    stage: Trial
    content_type: article
    language: uk

seo_metadata:
  primary_keyword: "діаграма Ганта для агенцій"
  secondary_keywords:
    - "gantt chart agencies"
    - "project timeline"
  search_volume: 1200
  keyword_density: "1.5%"
  humanization_score: "<25%"
  ai_overview_optimized: true
---
```

### Content Structure

```markdown
# H1 з Primary Keyword

## Introduction (150-200 слів)
Hook → Overview → Value prop

## H2: [Secondary Keyword 1]
### H3: Subtopic
Content з KB даними

## H2: [Secondary Keyword 2]
Content

## H2: TL;DR - Quick Summary
Bullet points (AI Overview optimization)

## H2: FAQ
Q&A format (featured snippets)

## Conclusion
Summary + CTA
```

---

## Шляхи збереження файлів

**Формат:**
```
/Content/[Stage]/[Category]/[Topic]/[Type]/filename.md
```

**Приклади:**

```
# Blog article про Gantt для Trial:
/Content/Trial/Features/Gantt_Chart/articles/gantt_agencies_tutorial_20241120.md

# Comparison Monday для Pre-Reg:
/Content/Pre-Registration/Competitors/Monday/Comparison/monday_alternative_guide_20241120.md

# Landing page Time Tracking:
/Content/Pre-Registration/Features/Time_Tracking/Landing_Page/time_tracking_feature_20241120.md

# SEO Brief (не в Content):
/SEO AGENT/generated/SEO_Brief_task_management_20241120.md
```

**Naming convention:**
```
[topic]_[business_type]_[content_type]_YYYYMMDD.md
```

---

## Workflow Decision Tree

```
Команда від користувача
    ↓
Parse parameters
    ↓
--seo або --seo-brief flag?
    ↓
YES → Load semantic CSV → Select keywords
NO  → Standard templates
    ↓
--seo-brief only?
    ↓
YES → Generate brief → Save to /SEO AGENT/generated/ → STOP
NO  → Continue
    ↓
WebSearch топ-10 → WebFetch pages → Create SEO Brief
    ↓
Read WS Knowledge Base (ICP, pains, stories)
    ↓
Select template (blog/landing/comparison)
    ↓
Apply humanization rules (MANDATORY for SEO)
    ↓
Generate content
    ↓
Save to /Content/[path]/
    ↓
User runs: python3 update_hubs.py
    ↓
DONE
```

---

## Приклади команд

### 1. Simple Article (без SEO mode)

```bash
/generate article about project management for remote teams
```

**Агент:**
- Topic: project management for remote teams
- Content type: article
- SEO mode: OFF
- Saves to: `/Content/Pre-Registration/Topics/Project_Management/Article/`

### 2. SEO Competitor Content

```bash
/generate --seo monday alternative for small teams
```

**Агент:**
1. Читає CSV семантики
2. Знаходить: "monday alternative" (1,200/mo), "monday competitor", etc.
3. Парсить топ-10 Google
4. Генерує humanized comparison article
5. Saves to: `/Content/Pre-Registration/Competitors/Monday/Comparison/`

### 3. SEO Brief Only

```bash
/generate --seo-brief best task management software 2025
```

**Агент:**
1. Keyword research з CSV
2. Аналіз топ-10
3. Генерує тільки brief
4. Saves to: `/SEO AGENT/generated/SEO_Brief_task_management_20241120.md`
5. Чекає на approval

### 4. Manual Keywords

```bash
/generate --seo landing page for gantt charts --keywords="gantt chart software,project timeline tool"
```

**Агент:**
- Пропускає CSV lookup
- Використовує надані keywords
- Генерує landing page

---

## Quality Checklist

### Для всього контенту:

- [ ] Правильний YAML frontmatter
- [ ] hierarchical_tags заповнені
- [ ] Реальні дані з KB (не вигадані)
- [ ] Правильний file path

### Для SEO контенту:

- [ ] Primary keyword з CSV
- [ ] 5-10 secondary keywords
- [ ] Keyword density 1-2%
- [ ] Гуманізація (contractions, varied sentences)
- [ ] AI detection <25%
- [ ] TL;DR section
- [ ] FAQ section
- [ ] seo_metadata в YAML

### Для SEO Brief:

- [ ] Primary keyword + search volume
- [ ] Secondary keywords list
- [ ] H1-H3 outline
- [ ] Word count recommendation
- [ ] Meta title/description

---

## Обмеження агента

### Технічні:

| Обмеження | Опис |
|-----------|------|
| Google US | Не українська видача |
| WebFetch | Деякі сайти блокують |
| CSV access | Може fail при великих файлах |

### Контентні:

| Обмеження | Рішення |
|-----------|---------|
| Не вигадує метрики | Тільки з KB |
| Не робить keyword research | Потрібен готовий інтент |
| Не перевіряє позиції | Тільки аналіз контенту |

---

## Error Handling

### Незрозуміла команда:

Агент питає: "I detected [X], is this correct? Please specify [missing parameter]"

### CSV не читається:

Fall back: "Would you like to provide keywords manually with --keywords?"

### Занадто широка тема:

Агент пропонує: "Consider specifying: [suggestions from semantic core]"

### Немає keywords в семантиці:

Агент показує: "Related terms from database: [list]. Should I proceed?"

---

## Що робить SEO-команда vs Agent

### Агент автоматизує:

- Збір даних з топ-10
- Keyword selection з CSV
- Генерацію першого драфту
- Структурування контенту
- Гуманізацію тексту
- Форматування YAML

### SEO-команда все ще потрібна для:

- Keyword research (визначення інтентів)
- Локальної оптимізації (UA специфіка)
- Технічного SEO
- Аналізу позицій
- Перевірки UA видачі (vs US)
- Фінальної редакції
- Link building стратегії

---

## Рекомендації для SEO-команди

### Перед генерацією:

1. **Визначте цільовий інтент** - один головний запит
2. **Перевірте семантику** - чи є в CSV потрібні keywords
3. **Виберіть стейдж** - Pre-Registration чи Trial
4. **Перевірте KB** - чи є дані для аудиторії

### Після генерації:

1. **Перевірте H2 структуру** - чи покриває топ-10
2. **Порівняйте з UA видачею** - ручний аналіз google.com.ua
3. **Додайте локальну семантику** - UA-специфічні запити
4. **Оптимізуйте мета-теги** - title, description
5. **Додайте внутрішні посилання**
6. **Перевірте AI detection** - target <25%

### Якщо US vs UA відрізняється:

1. Зробіть ручний аналіз топ-10 в google.com.ua
2. Порівняйте структуру H2 з US результатами
3. Скоригуйте контент якщо потрібно
4. Додайте локальні ключові слова

---

## Файли та ресурси

### Головні файли агента:

| Файл | Призначення |
|------|-------------|
| `/SEO AGENT/.claude/agents/seo-content-generator.md` | Головний промпт агента |
| `/SEO AGENT/command_parser.md` | Парсинг команд |
| `/SEO AGENT/semantic_processor.md` | Робота з CSV |
| `/SEO AGENT/integration_guide.md` | Інтеграція з Content Tree |

### Guidelines:

| Файл | Призначення |
|------|-------------|
| `/SEO AGENT/agent guidelines/naturalize-content-prompt.md` | Гуманізація |
| `/SEO AGENT/agent guidelines/Guide for creation TT for content.md` | SEO brief методологія |
| `/SEO AGENT/knowledge_base/seo_content_templates.md` | Шаблони |
| `/SEO AGENT/knowledge_base/content_optimization_rules.md` | SEO правила |

### Семантика:

| Файл | Опис |
|------|------|
| `/SEO AGENT/core semantic/WS semantic full.csv` | Повна база (2.3 MB) |
| `/SEO AGENT/core semantic/semantic core - competitors.csv` | Конкуренти |
| `/SEO AGENT/core semantic/semantic core - global (ua).csv` | UA market |

### Документація:

| Файл | Призначення |
|------|-------------|
| `/SEO AGENT/USAGE.md` | User documentation |
| `/.claude/commands/generate.md` | Команда генерації |
| `/docs/TEAM_GUIDE.md` | Main workflow |

---

## FAQ

### Чому Google US, а не UA?

Технічне обмеження WebSearch API. Для критичних статей робіть додатковий ручний аналіз UA видачі.

### Як часто оновлюється семантичне ядро?

CSV файли оновлюються вручну. Якщо потрібні нові keywords - додайте в `/SEO AGENT/core semantic/`.

### Чи можна змінити пошуковий запит?

Так. Використовуйте `--keywords="custom,keywords"` або інтерактивний режим.

### Що робити якщо агент не знайшов keywords?

1. Перевірте spelling
2. Спробуйте синоніми
3. Додайте keywords вручну через `--keywords`
4. Оновіть CSV якщо це важливий інтент

### Як перевірити AI detection score?

Використовуйте зовнішні інструменти:
- Originality.ai
- GPTZero
- Copyleaks

Target: <25%

### Агент замінює SEO-спеціаліста?

Ні. Агент - це інструмент для автоматизації рутини. SEO-спеціаліст потрібен для стратегії, локальної оптимізації, та технічного SEO.

---

## Контакти

- Питання по агенту → контент-команда Worksection
- Оновлення семантики → SEO-команда
- Баги та пропозиції → GitHub issues
