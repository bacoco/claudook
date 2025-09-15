#!/bin/bash
# Uninstall Claudook from current project or globally

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🗑️  Claudook Uninstaller${NC}"
echo "================================"

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

# Check for global installation
GLOBAL_DIR=""
if [ -d "$HOME/.claude/hooks/claudook" ]; then
    GLOBAL_DIR="$HOME/.claude"
fi

if [ -z "$PROJECT_DIR" ] && [ -z "$GLOBAL_DIR" ]; then
    echo -e "${YELLOW}⚠️  No Claudook installation found${NC}"
    exit 0
fi

# Show what was found
if [ -n "$PROJECT_DIR" ]; then
    echo -e "${BLUE}Found local Claudook in: ${PROJECT_DIR}${NC}"
fi
if [ -n "$GLOBAL_DIR" ]; then
    echo -e "${RED}Found GLOBAL Claudook in: ${GLOBAL_DIR}${NC}"
fi

echo
echo -e "${YELLOW}This will remove:${NC}"
echo "  • Claudook hook files"
echo "  • Settings.json (if contains claudook)"
echo "  • Task orchestration data"
echo "  • Analytics and backups"
echo "  • Control files (choices_enabled, tests_enabled, etc.)"
echo

# Ask for confirmation
if [ -n "$GLOBAL_DIR" ]; then
    echo -e "${RED}⚠️  WARNING: Global installation detected in ~/.claude/${NC}"
    read -p "$(echo -e ${RED}Remove GLOBAL Claudook installation? [y/N]: ${NC})" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        REMOVE_GLOBAL=true
    else
        REMOVE_GLOBAL=false
    fi
fi

if [ -n "$PROJECT_DIR" ]; then
    read -p "$(echo -e ${YELLOW}Remove LOCAL Claudook from this project? [y/N]: ${NC})" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        REMOVE_LOCAL=true
    else
        REMOVE_LOCAL=false
    fi
fi

# Function to clean a directory
clean_claudook() {
    local DIR=$1
    local TYPE=$2

    echo
    echo -e "${YELLOW}Removing ${TYPE} Claudook from ${DIR}...${NC}"

    # Remove claudook directory
    rm -rf "$DIR/.claude/hooks/claudook"
    echo "  ✓ Removed hooks/claudook/"

    # Remove settings.json if it contains claudook
    if [ -f "$DIR/.claude/settings.json" ]; then
        if grep -q "claudook" "$DIR/.claude/settings.json" 2>/dev/null; then
            rm -f "$DIR/.claude/settings.json"
            echo "  ✓ Removed settings.json"
        fi
    fi

    # Remove disabled settings
    rm -f "$DIR/.claude/settings.json.disabled" 2>/dev/null

    # Remove task data
    if [ -d "$DIR/.claude/tasks" ]; then
        rm -rf "$DIR/.claude/tasks"
        echo "  ✓ Removed tasks/"
    fi

    # Remove analytics
    if [ -d "$DIR/.claude/analytics" ]; then
        rm -rf "$DIR/.claude/analytics"
        echo "  ✓ Removed analytics/"
    fi

    # Remove control files
    rm -f "$DIR/.claude/choices_enabled" 2>/dev/null
    rm -f "$DIR/.claude/tests_enabled" 2>/dev/null
    rm -f "$DIR/.claude/parallel_enabled" 2>/dev/null

    # For global, also check home directory for control files
    if [ "$TYPE" = "GLOBAL" ]; then
        rm -f "$HOME/.claude/choices_enabled" 2>/dev/null
        rm -f "$HOME/.claude/tests_enabled" 2>/dev/null
        rm -f "$HOME/.claude/parallel_enabled" 2>/dev/null
    fi

    # Remove empty directories
    if [ -d "$DIR/.claude/commands" ]; then
        if [ -z "$(ls -A "$DIR/.claude/commands")" ]; then
            rmdir "$DIR/.claude/commands" 2>/dev/null
        fi
    fi

    if [ -d "$DIR/.claude/hooks" ]; then
        if [ -z "$(ls -A "$DIR/.claude/hooks")" ]; then
            rmdir "$DIR/.claude/hooks" 2>/dev/null
        fi
    fi

    # Only remove .claude if it's a local project directory
    if [ "$TYPE" = "LOCAL" ] && [ -d "$DIR/.claude" ]; then
        if [ -z "$(ls -A "$DIR/.claude")" ]; then
            rmdir "$DIR/.claude" 2>/dev/null
            echo "  ✓ Removed empty .claude/"
        fi
    fi

    echo -e "${GREEN}  ✅ ${TYPE} Claudook removed${NC}"
}

# Perform removal
if [ "$REMOVE_GLOBAL" = true ]; then
    clean_claudook "$HOME" "GLOBAL"
fi

if [ "$REMOVE_LOCAL" = true ]; then
    clean_claudook "$PROJECT_DIR" "LOCAL"
fi

if [ "$REMOVE_GLOBAL" != true ] && [ "$REMOVE_LOCAL" != true ]; then
    echo -e "${YELLOW}No changes made.${NC}"
    exit 0
fi

echo
echo -e "${GREEN}✅ Claudook successfully uninstalled${NC}"
echo
echo -e "${BLUE}To reinstall in a project:${NC}"
echo "  cd your-project/"
echo "  curl -fsSL https://raw.githubusercontent.com/bacoco/claudook/main/install.sh | bash"