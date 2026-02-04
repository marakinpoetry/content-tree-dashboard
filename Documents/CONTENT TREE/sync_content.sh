#!/bin/bash
# Two-way sync Content folder with Google Drive
# Usage: ./sync_content.sh [pull|push|both]

LOCAL="/Users/marakinpoetry/Documents/CONTENT TREE/Content"
REMOTE="wscontentdrive:Content"

# Exclude patterns (system files)
EXCLUDE="--exclude .DS_Store --exclude *.tmp --exclude ~*"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_help() {
    echo "Content Tree - Google Drive Sync"
    echo ""
    echo "Usage: ./sync_content.sh [command]"
    echo ""
    echo "Commands:"
    echo "  pull    Download changes from Google Drive (team's changes)"
    echo "  push    Upload changes to Google Drive (your changes)"
    echo "  both    Two-way sync (default)"
    echo "  status  Show what would change without syncing"
    echo ""
    echo "Examples:"
    echo "  ./sync_content.sh pull     # Get latest from team"
    echo "  ./sync_content.sh push     # Push your new content"
    echo "  ./sync_content.sh          # Full two-way sync"
}

update_db() {
    echo -e "${BLUE}Updating SQLite database...${NC}"
    cd "/Users/marakinpoetry/Documents/CONTENT TREE"
    python3 scripts/db/sync.py 2>&1 || echo -e "Warning: db sync failed"
    if [ -f scripts/db/export.py ]; then
        python3 scripts/db/export.py 2>&1 || echo -e "Warning: db export failed"
    fi
    echo -e "${GREEN}✓ Database updated${NC}"
}

pull_changes() {
    echo -e "${BLUE}Downloading changes from Google Drive...${NC}"
    rclone copy "$REMOTE" "$LOCAL" --update --verbose $EXCLUDE 2>&1 || true
    echo -e "${GREEN}✓ Pull complete${NC}"
    update_db
}

push_changes() {
    echo -e "${BLUE}Uploading changes to Google Drive...${NC}"
    rclone copy "$LOCAL" "$REMOTE" --update --verbose $EXCLUDE
    echo -e "${GREEN}✓ Push complete${NC}"
}

show_status() {
    echo -e "${BLUE}Changes that would be downloaded (dry run):${NC}"
    rclone copy "$REMOTE" "$LOCAL" --update --dry-run $EXCLUDE 2>&1 || true
    echo ""
    echo -e "${BLUE}Changes that would be uploaded (dry run):${NC}"
    rclone copy "$LOCAL" "$REMOTE" --update --dry-run $EXCLUDE
}

# Main
case "${1:-both}" in
    pull)
        pull_changes
        ;;
    push)
        push_changes
        ;;
    both)
        echo -e "${BLUE}Starting two-way sync...${NC}"
        echo ""
        pull_changes
        echo ""
        push_changes
        echo ""
        echo -e "${GREEN}✓ Sync complete!${NC}"
        ;;
    status)
        show_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
