#!/usr/bin/env python3
"""
Content Samples Analyzer
Аналізує існуючі файли контенту та створює шаблони стилю для кожного типу.
"""

import os
import re
import yaml
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

# Кореневі папки для аналізу
CONTENT_ROOT = Path("/Users/marakinpoetry/Documents/CONTENT TREE/Content")
STAGES = ["Pre-Registration", "Trial", "Success_Client"]
CATEGORIES = ["Features", "Business_Types", "Competitors", "PM_Education", "Pains"]
CONTENT_TYPES = ["articles", "videos", "ads", "landings", "Case_Study", "SMM"]


def extract_frontmatter(content: str) -> Tuple[Dict, str]:
    """Витягує YAML frontmatter та основний контент."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if match:
        try:
            frontmatter = yaml.safe_load(match.group(1))
            body = match.group(2)
            return frontmatter, body
        except:
            return {}, content
    return {}, content


def analyze_structure(body: str) -> Dict:
    """Аналізує структуру контенту."""
    lines = body.strip().split('\n')

    # Визначаємо заголовки
    h1_headers = re.findall(r'^# (.+)$', body, re.MULTILINE)
    h2_headers = re.findall(r'^## (.+)$', body, re.MULTILINE)
    h3_headers = re.findall(r'^### (.+)$', body, re.MULTILINE)

    # Рахуємо параграфи (блоки тексту)
    paragraphs = [p for p in body.split('\n\n') if p.strip() and not p.strip().startswith('#')]

    # Рахуємо слова
    words = len(body.split())

    # Визначаємо середню довжину параграфа
    avg_paragraph_length = sum(len(p.split()) for p in paragraphs) / len(paragraphs) if paragraphs else 0

    # Шукаємо списки
    bullet_lists = len(re.findall(r'^\s*[-*]\s', body, re.MULTILINE))
    numbered_lists = len(re.findall(r'^\s*\d+\.\s', body, re.MULTILINE))

    # Шукаємо цитати
    quotes = len(re.findall(r'^>\s', body, re.MULTILINE))

    # Шукаємо посилання
    links = len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', body))

    # Шукаємо виклики до дії (CTA)
    cta_patterns = [
        r'спробуй',
        r'спробувати',
        r'зареєструй',
        r'почни',
        r'отримай',
        r'замовити',
        r'try\s',
        r'start\s',
        r'get\s',
        r'register',
        r'попробуй'
    ]
    cta_count = sum(len(re.findall(pattern, body, re.IGNORECASE)) for pattern in cta_patterns)

    return {
        "h1_count": len(h1_headers),
        "h2_count": len(h2_headers),
        "h3_count": len(h3_headers),
        "h1_headers": h1_headers[:3],  # Перші 3 для прикладу
        "h2_headers": h2_headers[:5],  # Перші 5 для прикладу
        "paragraph_count": len(paragraphs),
        "word_count": words,
        "avg_paragraph_length": round(avg_paragraph_length),
        "bullet_lists": bullet_lists,
        "numbered_lists": numbered_lists,
        "quotes": quotes,
        "links": links,
        "cta_count": cta_count
    }


def analyze_tone_and_style(body: str) -> Dict:
    """Аналізує тон та стиль написання."""

    # Перевірка на формальність (використання "Ви" vs "ти")
    formal_pronouns = len(re.findall(r'\b(Ви|Вас|Вам|Вами|You|you)\b', body))
    informal_pronouns = len(re.findall(r'\b(ти|тобі|тебе|тобою|ты|тебя|тебе)\b', body))

    # Емоційність (знаки оклику)
    exclamation_marks = body.count('!')

    # Питальність
    question_marks = body.count('?')

    # Технічність (наявність технічних термінів)
    technical_terms = [
        'API', 'інтеграція', 'функція', 'налаштування', 'конфігурація',
        'integration', 'function', 'configuration', 'settings',
        'интеграция', 'функция', 'настройки'
    ]
    technical_count = sum(body.lower().count(term.lower()) for term in technical_terms)

    # Використання цифр та метрик
    numbers = len(re.findall(r'\b\d+%', body))

    # Довжина речень (складність)
    sentences = re.split(r'[.!?]+', body)
    avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / len([s for s in sentences if s.strip()])

    tone = "formal" if formal_pronouns > informal_pronouns else "informal"
    emotion_level = "high" if exclamation_marks > 5 else "medium" if exclamation_marks > 2 else "low"
    technical_level = "high" if technical_count > 10 else "medium" if technical_count > 5 else "low"

    return {
        "tone": tone,
        "emotion_level": emotion_level,
        "technical_level": technical_level,
        "exclamation_marks": exclamation_marks,
        "question_marks": question_marks,
        "metrics_count": numbers,
        "avg_sentence_length": round(avg_sentence_length, 1)
    }


def analyze_file(file_path: Path) -> Dict:
    """Аналізує один файл."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        frontmatter, body = extract_frontmatter(content)
        structure = analyze_structure(body)
        style = analyze_tone_and_style(body)

        return {
            "file_path": str(file_path.relative_to(CONTENT_ROOT)),
            "frontmatter": frontmatter,
            "structure": structure,
            "style": style,
            "success": True
        }
    except Exception as e:
        return {
            "file_path": str(file_path),
            "error": str(e),
            "success": False
        }


def get_sample_files(category_path: Path, content_type: str, limit: int = 2) -> List[Path]:
    """Отримує приклади файлів з папки."""
    content_type_path = category_path / content_type

    if not content_type_path.exists():
        return []

    # Шукаємо .md файли
    md_files = list(content_type_path.glob("*.md"))

    # Якщо файлів більше limit, беремо найновіші
    if len(md_files) > limit:
        md_files = sorted(md_files, key=lambda x: x.stat().st_mtime, reverse=True)[:limit]

    return md_files


def aggregate_analysis(analyses: List[Dict]) -> Dict:
    """Агрегує результати аналізу кількох файлів."""
    if not analyses:
        return {}

    # Середні значення структури
    structure_keys = ["h1_count", "h2_count", "h3_count", "paragraph_count",
                     "word_count", "avg_paragraph_length", "bullet_lists",
                     "numbered_lists", "quotes", "links", "cta_count"]

    aggregated = {
        "sample_count": len(analyses),
        "structure": {},
        "style": {}
    }

    # Агрегація структури
    for key in structure_keys:
        values = [a["structure"][key] for a in analyses if a.get("success")]
        if values:
            aggregated["structure"][key] = {
                "min": min(values),
                "max": max(values),
                "avg": round(sum(values) / len(values), 1)
            }

    # Збираємо приклади заголовків
    all_h2 = []
    for a in analyses:
        if a.get("success"):
            all_h2.extend(a["structure"].get("h2_headers", []))
    aggregated["structure"]["h2_examples"] = list(set(all_h2))[:10]

    # Агрегація стилю
    tones = [a["style"]["tone"] for a in analyses if a.get("success")]
    emotions = [a["style"]["emotion_level"] for a in analyses if a.get("success")]
    technical = [a["style"]["technical_level"] for a in analyses if a.get("success")]

    aggregated["style"] = {
        "dominant_tone": max(set(tones), key=tones.count) if tones else "unknown",
        "dominant_emotion": max(set(emotions), key=emotions.count) if emotions else "unknown",
        "dominant_technical": max(set(technical), key=technical.count) if technical else "unknown",
        "avg_sentence_length": round(sum(a["style"]["avg_sentence_length"] for a in analyses if a.get("success")) / len(analyses), 1)
    }

    # Збираємо приклади frontmatter
    frontmatters = [a["frontmatter"] for a in analyses if a.get("success") and a.get("frontmatter")]
    if frontmatters:
        aggregated["frontmatter_example"] = frontmatters[0]

    return aggregated


def scan_content_tree():
    """Сканує всю Content Tree та аналізує контент."""
    results = defaultdict(lambda: defaultdict(list))

    print("🔍 Сканую Content Tree...")
    print()

    for stage in STAGES:
        stage_path = CONTENT_ROOT / stage
        if not stage_path.exists():
            continue

        print(f"📂 Stage: {stage}")

        for category in CATEGORIES:
            category_path = stage_path / category
            if not category_path.exists():
                continue

            print(f"  📁 Category: {category}")

            # Шукаємо всі підпапки (теми)
            for topic_path in category_path.iterdir():
                if not topic_path.is_dir():
                    continue

                topic_name = topic_path.name

                # Для кожного типу контенту
                for content_type in CONTENT_TYPES:
                    sample_files = get_sample_files(topic_path, content_type, limit=2)

                    if not sample_files:
                        continue

                    print(f"    📄 {content_type}: {len(sample_files)} samples from {topic_name}")

                    analyses = []
                    for file_path in sample_files:
                        analysis = analyze_file(file_path)
                        if analysis["success"]:
                            analyses.append(analysis)

                    if analyses:
                        key = f"{stage}_{category}_{content_type}"
                        results[key]["analyses"] = analyses
                        results[key]["aggregated"] = aggregate_analysis(analyses)
                        results[key]["stage"] = stage
                        results[key]["category"] = category
                        results[key]["content_type"] = content_type

    print()
    print(f"✅ Проаналізовано {len(results)} комбінацій контенту")
    return dict(results)


def generate_template_markdown(results: Dict) -> str:
    """Генерує CONTENT_TEMPLATES.md на основі аналізу."""

    md = """# Content Templates & Style Guide
Автоматично згенеровано на основі аналізу існуючих файлів контенту.

Цей файл містить шаблони та рекомендації для генерації контенту, схожого на існуючі приклади.

---

"""

    # Групуємо за типом контенту
    by_content_type = defaultdict(list)
    for key, data in results.items():
        content_type = data["content_type"]
        by_content_type[content_type].append((key, data))

    for content_type, items in sorted(by_content_type.items()):
        md += f"\n## {content_type.upper()}\n\n"

        for key, data in items:
            stage = data["stage"]
            category = data["category"]
            agg = data["aggregated"]

            md += f"### {stage} / {category}\n\n"
            md += f"**Базується на {agg['sample_count']} реальних прикладах**\n\n"

            # Структура
            md += "#### 📊 Структура\n\n"
            struct = agg["structure"]

            md += f"- **Довжина**: {struct.get('word_count', {}).get('min', 0)} - {struct.get('word_count', {}).get('max', 0)} слів "
            md += f"(середнє: {struct.get('word_count', {}).get('avg', 0)})\n"

            md += f"- **Заголовки H2**: {struct.get('h2_count', {}).get('min', 0)} - {struct.get('h2_count', {}).get('max', 0)} "
            md += f"(середнє: {struct.get('h2_count', {}).get('avg', 0)})\n"

            md += f"- **Параграфів**: {struct.get('paragraph_count', {}).get('min', 0)} - {struct.get('paragraph_count', {}).get('max', 0)}\n"

            md += f"- **Середня довжина параграфа**: ~{struct.get('avg_paragraph_length', {}).get('avg', 0)} слів\n"

            if struct.get('bullet_lists', {}).get('avg', 0) > 0:
                md += f"- **Маркові списки**: присутні (~{struct.get('bullet_lists', {}).get('avg', 0)} пунктів)\n"

            if struct.get('cta_count', {}).get('avg', 0) > 0:
                md += f"- **CTA (заклики до дії)**: ~{struct.get('cta_count', {}).get('avg', 0)} разів\n"

            # Приклади заголовків H2
            if struct.get("h2_examples"):
                md += "\n**Типові заголовки H2:**\n"
                for h2 in struct["h2_examples"][:5]:
                    md += f"- {h2}\n"

            md += "\n"

            # Стиль
            md += "#### 🎨 Стиль та тон\n\n"
            style = agg["style"]

            tone_map = {
                "formal": "Формальний (Ви)",
                "informal": "Неформальний (ти)"
            }
            md += f"- **Тон**: {tone_map.get(style['dominant_tone'], style['dominant_tone'])}\n"

            emotion_map = {
                "high": "Високий (багато емоцій, знаків оклику)",
                "medium": "Середній (помірна емоційність)",
                "low": "Низький (стриманий, фактологічний)"
            }
            md += f"- **Емоційність**: {emotion_map.get(style['dominant_emotion'], style['dominant_emotion'])}\n"

            tech_map = {
                "high": "Високий (багато технічних термінів)",
                "medium": "Середній (баланс технічності та доступності)",
                "low": "Низький (доступна мова для широкої аудиторії)"
            }
            md += f"- **Технічність**: {tech_map.get(style['dominant_technical'], style['dominant_technical'])}\n"

            md += f"- **Середня довжина речення**: {style['avg_sentence_length']} слів\n"

            md += "\n"

            # Frontmatter приклад
            if agg.get("frontmatter_example"):
                md += "#### 📝 Приклад YAML Frontmatter\n\n"
                md += "```yaml\n"
                md += yaml.dump(agg["frontmatter_example"], allow_unicode=True, default_flow_style=False)
                md += "```\n\n"

            md += "---\n\n"

    # Додаємо загальні рекомендації
    md += """
## 🎯 Загальні рекомендації для генерації

### Принципи схожості

1. **Читай перед генерацією**: Завжди читай 1-2 приклади з цільової папки перед генерацією
2. **Копіюй структуру**: Використовуй таку саму структуру заголовків та розділів
3. **Відтворюй тон**: Збережи формальність/неформальність, емоційність, технічність
4. **Дотримуйся довжини**: Генеруй текст приблизно такої самої довжини як приклади
5. **Використовуй реальні дані**: Тільки з Knowledge Base, ніколи не вигадуй метрики

### Smart Mix Formula

```
Згенерований контент = PROMPTS.md (структура) + Реальні приклади (стиль) + Knowledge Base (дані)
```

### Інструкція для Claude

При генерації контенту:

1. Прочитай відповідний промпт з PROMPTS.md
2. Прочитай 1-2 реальні файли з цільової папки
3. Витягни з них:
   - Структуру розділів (H1, H2, H3)
   - Тон звертання (Ви чи ти)
   - Рівень емоційності
   - Рівень технічності
   - Типову довжину параграфів
4. Згенеруй контент який виглядає ТАК САМО як приклади, але містить нову інформацію
5. Використовуй ТІЛЬКИ реальні дані з Knowledge Base

### Перевірка якості

Після генерації контент повинен:
- ✅ Мати схожу структуру з прикладами
- ✅ Містити реальні метрики з KB
- ✅ Мати правильні hierarchical_tags
- ✅ Відповідати тону та стилю прикладів
- ✅ Бути такої самої довжини (±20%)
"""

    return md


def main():
    """Головна функція."""
    print("=" * 60)
    print("Content Samples Analyzer")
    print("=" * 60)
    print()

    # Сканування та аналіз
    results = scan_content_tree()

    # Генерація шаблонів
    print()
    print("📝 Генерую CONTENT_TEMPLATES.md...")
    template_md = generate_template_markdown(results)

    # Збереження
    output_path = Path("/Users/marakinpoetry/Documents/CONTENT TREE/docs/CONTENT_TEMPLATES.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template_md)

    print(f"✅ Збережено: {output_path}")
    print()
    print("=" * 60)
    print("Готово! Тепер можна використовувати CONTENT_TEMPLATES.md")
    print("для генерації контенту схожого на існуючі приклади.")
    print("=" * 60)


if __name__ == "__main__":
    main()
