#!/bin/bash
# Real-time sync: watches local folder and polls Google Drive
# Usage: ./watch_and_sync.sh [start|stop|status]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOCAL="$SCRIPT_DIR/Content"
REMOTE="wscontentdrive:Content"
EXCLUDE="--exclude .DS_Store --exclude *.tmp --exclude ~*"
LOG_FILE="$SCRIPT_DIR/.sync.log"
PID_FILE="$SCRIPT_DIR/.sync.pid"
POLL_INTERVAL=300  # 5 minutes for Drive polling

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    echo "$1"
}

push_changes() {
    log "⬆️  Pushing local changes to Drive..."
    rclone copy "$LOCAL" "$REMOTE" --update $EXCLUDE --quiet
    log "✓ Push complete"
}

pull_changes() {
    rclone copy "$REMOTE" "$LOCAL" --update $EXCLUDE --quiet 2>/dev/null
}

# Watch local folder and push on changes
watch_local() {
    log "👁️  Watching local folder for changes..."
    fswatch -o "$LOCAL" --exclude '\.DS_Store$' --exclude '\.tmp$' | while read -r count; do
        sleep 2  # Wait for file to finish writing
        push_changes
    done
}

# Poll Google Drive for changes
poll_drive() {
    log "🔄 Polling Drive every $((POLL_INTERVAL/60)) minutes..."
    while true; do
        sleep $POLL_INTERVAL
        log "⬇️  Checking Drive for team changes..."
        pull_changes
    done
}

start_sync() {
    if [ -f "$PID_FILE" ]; then
        echo "Sync already running (PID: $(cat "$PID_FILE"))"
        echo "Use './watch_and_sync.sh stop' to stop it first"
        exit 1
    fi

    log "🚀 Starting real-time sync..."

    # Initial sync
    log "📥 Initial pull from Drive..."
    pull_changes
    log "📤 Initial push to Drive..."
    push_changes

    # Start watchers in background
    watch_local &
    WATCH_PID=$!

    poll_drive &
    POLL_PID=$!

    echo "$WATCH_PID $POLL_PID" > "$PID_FILE"

    log "✅ Sync running (PIDs: $WATCH_PID, $POLL_PID)"
    log "   Local changes → instant push"
    log "   Drive changes → checked every 5 min"
    echo ""
    echo "Logs: $LOG_FILE"
    echo "Stop: ./watch_and_sync.sh stop"

    # Keep script running
    wait
}

stop_sync() {
    if [ ! -f "$PID_FILE" ]; then
        echo "Sync not running"
        exit 0
    fi

    read -r PIDS < "$PID_FILE"
    for pid in $PIDS; do
        kill "$pid" 2>/dev/null
    done

    # Kill any remaining fswatch processes
    pkill -f "fswatch.*$LOCAL" 2>/dev/null

    rm -f "$PID_FILE"
    log "🛑 Sync stopped"
}

show_status() {
    if [ -f "$PID_FILE" ]; then
        echo "✅ Sync running (PIDs: $(cat "$PID_FILE"))"
        echo "Logs: tail -f $LOG_FILE"
    else
        echo "⏹️  Sync not running"
        echo "Start: ./watch_and_sync.sh start"
    fi
}

case "${1:-start}" in
    start)
        start_sync
        ;;
    stop)
        stop_sync
        ;;
    status)
        show_status
        ;;
    *)
        echo "Usage: ./watch_and_sync.sh [start|stop|status]"
        exit 1
        ;;
esac
