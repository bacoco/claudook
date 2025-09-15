#!/bin/bash
# Uninstall Claudook from current project only

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🗑️  Claudook Uninstaller (Current Project)${NC}"
echo "========================================="

# Find project root
CURRENT_DIR=$(pwd)
PROJECT_DIR=""

while [ "$CURRENT_DIR" != "/" ]; do
    if [ -d "$CURRENT_DIR/.claude/hooks/claudook" ]; then
        PROJECT_DIR="$CURRENT_DIR"
        break
    fi
    CURRENT_DIR=$(dirname "$CURRENT_DIR")
done

if [ -z "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}⚠️  No Claudook installation found in current project${NC}"
    exit 0
fi

echo -e "${BLUE}Found Claudook in: ${PROJECT_DIR}${NC}"
echo
echo -e "${YELLOW}This will remove:${NC}"
echo "  • Claudook hook files"
echo "  • Local settings.json"
echo "  • Task orchestration data"
echo "  • Analytics and backups"
echo

# Ask for confirmation
read -p "$(echo -e ${RED}Remove Claudook from this project? [y/N]: ${NC})" -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Cancelled. No changes made.${NC}"
    exit 0
fi

echo
echo -e "${YELLOW}Removing Claudook...${NC}"

# Remove claudook directory
rm -rf "$PROJECT_DIR/.claude/hooks/claudook"
echo "  ✓ Removed hooks/claudook/"

# Remove settings.json if it contains claudook
if [ -f "$PROJECT_DIR/.claude/settings.json" ]; then
    if grep -q "claudook" "$PROJECT_DIR/.claude/settings.json" 2>/dev/null; then
        rm -f "$PROJECT_DIR/.claude/settings.json"
        echo "  ✓ Removed settings.json"
    fi
fi

# Remove disabled settings
rm -f "$PROJECT_DIR/.claude/settings.json.disabled" 2>/dev/null

# Remove task data
if [ -d "$PROJECT_DIR/.claude/tasks" ]; then
    rm -rf "$PROJECT_DIR/.claude/tasks"
    echo "  ✓ Removed tasks/"
fi

# Remove analytics
if [ -d "$PROJECT_DIR/.claude/analytics" ]; then
    rm -rf "$PROJECT_DIR/.claude/analytics"
    echo "  ✓ Removed analytics/"
fi

# Remove control files
rm -f "$PROJECT_DIR/.claude/choices_enabled" 2>/dev/null
rm -f "$PROJECT_DIR/.claude/tests_enabled" 2>/dev/null
rm -f "$PROJECT_DIR/.claude/parallel_enabled" 2>/dev/null

# Remove empty directories
if [ -d "$PROJECT_DIR/.claude/commands" ]; then
    if [ -z "$(ls -A "$PROJECT_DIR/.claude/commands")" ]; then
        rmdir "$PROJECT_DIR/.claude/commands" 2>/dev/null
    fi
fi

if [ -d "$PROJECT_DIR/.claude/hooks" ]; then
    if [ -z "$(ls -A "$PROJECT_DIR/.claude/hooks")" ]; then
        rmdir "$PROJECT_DIR/.claude/hooks" 2>/dev/null
    fi
fi

if [ -d "$PROJECT_DIR/.claude" ]; then
    if [ -z "$(ls -A "$PROJECT_DIR/.claude")" ]; then
        rmdir "$PROJECT_DIR/.claude" 2>/dev/null
        echo "  ✓ Removed empty .claude/"
    fi
fi

echo
echo -e "${GREEN}✅ Claudook successfully uninstalled from ${PROJECT_DIR}${NC}"
echo
echo -e "${BLUE}To reinstall:${NC}"
echo "  curl -fsSL https://raw.githubusercontent.com/bacoco/claudook/main/install.sh | bash"