#!/bin/bash
# Uninstall all Claudook instances from your system

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Claudook Uninstaller${NC}"
echo "================================"

# Find all .claude directories (excluding home directory)
echo -e "${YELLOW}Searching for Claudook installations...${NC}"

# Start from current directory or provided path
SEARCH_PATH="${1:-$(pwd)}"

# Find all .claude directories that contain claudook
CLAUDOOK_DIRS=$(find "$SEARCH_PATH" -type d -path "*/.claude/hooks/claudook" 2>/dev/null | grep -v "$HOME/.claude")

if [ -z "$CLAUDOOK_DIRS" ]; then
    echo -e "${GREEN}✅ No Claudook installations found${NC}"
    exit 0
fi

# Count installations
COUNT=$(echo "$CLAUDOOK_DIRS" | wc -l | tr -d ' ')
echo -e "${BLUE}Found ${COUNT} Claudook installation(s):${NC}"
echo

# List all found installations
echo "$CLAUDOOK_DIRS" | while read -r dir; do
    PROJECT_DIR=$(dirname $(dirname $(dirname "$dir")))
    echo -e "  📁 $PROJECT_DIR"
done

echo
echo -e "${YELLOW}⚠️  This will remove:${NC}"
echo "  - All Claudook hook files"
echo "  - Local settings.json files"
echo "  - Task orchestration files"
echo "  - Analytics and backup data"
echo

# Ask for confirmation
read -p "$(echo -e ${RED}Are you sure you want to remove ALL Claudook installations? [y/N]: ${NC})" -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Cancelled. No changes made.${NC}"
    exit 0
fi

# Remove each installation
echo
echo -e "${YELLOW}Removing Claudook installations...${NC}"

echo "$CLAUDOOK_DIRS" | while read -r dir; do
    PROJECT_DIR=$(dirname $(dirname $(dirname "$dir")))
    echo -e "${BLUE}Cleaning: $PROJECT_DIR${NC}"

    # Remove claudook directory
    rm -rf "$dir"
    echo "  ✓ Removed hooks/claudook/"

    # Remove settings.json if it exists
    SETTINGS_FILE="$PROJECT_DIR/.claude/settings.json"
    if [ -f "$SETTINGS_FILE" ]; then
        # Check if settings.json contains claudook references
        if grep -q "claudook" "$SETTINGS_FILE" 2>/dev/null; then
            rm -f "$SETTINGS_FILE"
            echo "  ✓ Removed settings.json"
        fi
    fi

    # Remove disabled settings if exists
    rm -f "$PROJECT_DIR/.claude/settings.json.disabled" 2>/dev/null

    # Remove task orchestration data
    if [ -d "$PROJECT_DIR/.claude/tasks" ]; then
        rm -rf "$PROJECT_DIR/.claude/tasks"
        echo "  ✓ Removed tasks/"
    fi

    # Remove analytics data
    if [ -d "$PROJECT_DIR/.claude/analytics" ]; then
        rm -rf "$PROJECT_DIR/.claude/analytics"
        echo "  ✓ Removed analytics/"
    fi

    # Remove control files
    rm -f "$PROJECT_DIR/.claude/choices_enabled" 2>/dev/null
    rm -f "$PROJECT_DIR/.claude/tests_enabled" 2>/dev/null
    rm -f "$PROJECT_DIR/.claude/parallel_enabled" 2>/dev/null

    # Remove commands directory if empty
    if [ -d "$PROJECT_DIR/.claude/commands" ]; then
        if [ -z "$(ls -A "$PROJECT_DIR/.claude/commands")" ]; then
            rmdir "$PROJECT_DIR/.claude/commands" 2>/dev/null
        fi
    fi

    # Remove .claude directory if empty
    if [ -d "$PROJECT_DIR/.claude" ]; then
        if [ -z "$(ls -A "$PROJECT_DIR/.claude")" ]; then
            rmdir "$PROJECT_DIR/.claude" 2>/dev/null
            echo "  ✓ Removed empty .claude/"
        fi
    fi

    echo -e "${GREEN}  ✅ Cleaned${NC}"
    echo
done

# Final summary
echo -e "${GREEN}✅ Successfully removed ${COUNT} Claudook installation(s)${NC}"
echo
echo -e "${BLUE}To reinstall Claudook in a project:${NC}"
echo "  cd your-project/"
echo "  curl -fsSL https://raw.githubusercontent.com/bacoco/claudook/main/install.sh | bash"