.PHONY: update publish dashboard dashboard-stop all help sync sync-pull sync-push sync-status sync-watch sync-watch-stop sync-watch-status sync-db export-dashboard search

# Оновлює всі 59 Hub файлів
update:
	@echo "🔄 Оновлюю Hub навігацію..."
	@cd "/Users/marakinpoetry/Documents/CONTENT TREE" && python3 update_hubs.py
	@echo "✅ Hub навігацію оновлено"

# Публікує контент в WordPress CMS
publish:
	@echo "📤 Публікую контент в CMS..."
	@cd "/Users/marakinpoetry/Documents/CONTENT TREE" && python3 scripts/publish_to_cms.py
	@echo "✅ Контент опубліковано"

# Запускає Dashboard на localhost:8080
dashboard:
	@echo "📊 Запускаю Dashboard..."
	@cd "/Users/marakinpoetry/Documents/CONTENT TREE" && ./Dashboard/start_dashboard.sh
	@echo "✅ Dashboard доступний на http://localhost:8080"

# Зупиняє Dashboard
dashboard-stop:
	@echo "🛑 Зупиняю Dashboard..."
	@cd "/Users/marakinpoetry/Documents/CONTENT TREE" && ./Dashboard/stop_dashboard.sh
	@echo "✅ Dashboard зупинено"

# Оновлює хаби + публікує
all: update publish

# Google Drive Sync - двосторонній
sync:
	@echo "🔄 Синхронізую з Google Drive..."
	@cd "/Users/marakinpoetry/Documents/CONTENT TREE" && ./sync_content.sh both

# Google Drive Sync - тільки завантаження
sync-pull:
	@echo "⬇️  Завантажую зміни команди з Google Drive..."
	@cd "/Users/marakinpoetry/Documents/CONTENT TREE" && ./sync_content.sh pull

# Google Drive Sync - тільки вивантаження
sync-push:
	@echo "⬆️  Вивантажую мої зміни в Google Drive..."
	@cd "/Users/marakinpoetry/Documents/CONTENT TREE" && ./sync_content.sh push

# Google Drive Sync - перегляд змін
sync-status:
	@echo "👀 Перегляд змін (dry run)..."
	@cd "/Users/marakinpoetry/Documents/CONTENT TREE" && ./sync_content.sh status

# Real-time sync - запустити
sync-watch:
	@cd "/Users/marakinpoetry/Documents/CONTENT TREE" && ./watch_and_sync.sh start

# Real-time sync - зупинити
sync-watch-stop:
	@cd "/Users/marakinpoetry/Documents/CONTENT TREE" && ./watch_and_sync.sh stop

# Real-time sync - статус
sync-watch-status:
	@cd "/Users/marakinpoetry/Documents/CONTENT TREE" && ./watch_and_sync.sh status

# Синхронізувати Content/ → SQLite
sync-db:
	@echo "🗄️  Синхронізую Content/ → SQLite..."
	@cd "/Users/marakinpoetry/Documents/CONTENT TREE" && python3 scripts/db/sync.py
	@echo "✅ База даних оновлена"

# Експорт SQLite → data.json (для Dashboard)
export-dashboard:
	@echo "📊 Експортую дані для Dashboard..."
	@cd "/Users/marakinpoetry/Documents/CONTENT TREE" && python3 scripts/db/export.py
	@echo "✅ data.json оновлено"

# Пошук по контенту
search:
	@cd "/Users/marakinpoetry/Documents/CONTENT TREE" && python3 scripts/db/search.py $(q) $(ARGS)

# Показує всі доступні команди
help:
	@echo ""
	@echo "📋 Доступні команди Content Tree:"
	@echo ""
	@echo "  make update         - Оновити Hub навігацію (59 хабів)"
	@echo "  make publish        - Опублікувати контент в WordPress CMS"
	@echo "  make dashboard      - Запустити Dashboard (localhost:8080)"
	@echo "  make dashboard-stop - Зупинити Dashboard"
	@echo "  make all            - Оновити хаби + опублікувати"
	@echo ""
	@echo "  make sync           - Двостороння синхронізація з Google Drive"
	@echo "  make sync-pull      - Завантажити зміни команди"
	@echo "  make sync-push      - Вивантажити мої зміни"
	@echo "  make sync-status    - Перегляд змін без синхронізації"
	@echo ""
	@echo "  make sync-watch     - Запустити real-time синхронізацію"
	@echo "  make sync-watch-stop  - Зупинити real-time синхронізацію"
	@echo "  make sync-watch-status - Статус real-time синхронізації"
	@echo ""
	@echo "  make sync-db        - Синхронізувати Content/ → SQLite"
	@echo "  make export-dashboard - Експорт SQLite → data.json"
	@echo "  make search q=\"gantt\" - Пошук по контенту"
	@echo ""
	@echo "  make help           - Показати цю довідку"
	@echo ""
