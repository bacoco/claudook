#!/bin/bash
# Find and remove ALL Claudook instances from your system

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Claudook System-Wide Finder & Remover${NC}"
echo "=========================================="

# Start from current directory or provided path
SEARCH_PATH="${1:-$(pwd)}"

echo -e "${YELLOW}Searching for Claudook installations...${NC}"
echo -e "${BLUE}Search path: ${SEARCH_PATH}${NC}"

# Ask about search scope
echo
echo -e "${YELLOW}Choose search scope:${NC}"
echo "  1) Current directory only ($(basename $SEARCH_PATH))"
echo "  2) Current directory and subdirectories (default)"
echo "  3) Parent directory and all subdirectories"
echo "  4) Home directory (slow, comprehensive)"
echo

read -p "$(echo -e ${BLUE}Select option [1-4, default=2]: ${NC})" -n 1 SCOPE
echo

case "$SCOPE" in
    1)
        SEARCH_DEPTH="-maxdepth 3"
        echo -e "${GREEN}Searching current directory only...${NC}"
        ;;
    3)
        SEARCH_PATH="$(dirname $SEARCH_PATH)"
        SEARCH_DEPTH=""
        echo -e "${GREEN}Searching from parent: ${SEARCH_PATH}${NC}"
        ;;
    4)
        SEARCH_PATH="$HOME"
        SEARCH_DEPTH=""
        echo -e "${YELLOW}⚠️  Searching entire home directory (this may take a while)...${NC}"
        ;;
    *)
        SEARCH_DEPTH=""
        echo -e "${GREEN}Searching current directory and subdirectories...${NC}"
        ;;
esac

echo

# Find all .claude directories that contain claudook
CLAUDOOK_DIRS=$(find "$SEARCH_PATH" $SEARCH_DEPTH -type d -path "*/.claude/hooks/claudook" 2>/dev/null)

# Check global installation separately
GLOBAL_FOUND=false
if [ -d "$HOME/.claude/hooks/claudook" ]; then
    GLOBAL_FOUND=true
    # Add to list if not already included
    if ! echo "$CLAUDOOK_DIRS" | grep -q "$HOME/.claude/hooks/claudook"; then
        if [ -z "$CLAUDOOK_DIRS" ]; then
            CLAUDOOK_DIRS="$HOME/.claude/hooks/claudook"
        else
            CLAUDOOK_DIRS="$CLAUDOOK_DIRS"$'\n'"$HOME/.claude/hooks/claudook"
        fi
    fi
fi

if [ -z "$CLAUDOOK_DIRS" ]; then
    echo -e "${GREEN}✅ No Claudook installations found${NC}"
    exit 0
fi

# Count installations
COUNT=$(echo "$CLAUDOOK_DIRS" | grep -c .)
echo -e "${BLUE}Found ${COUNT} Claudook installation(s):${NC}"
echo

# List all found installations
echo "$CLAUDOOK_DIRS" | while read -r dir; do
    PROJECT_DIR=$(dirname $(dirname $(dirname "$dir")))
    if [ "$PROJECT_DIR" = "$HOME" ]; then
        echo -e "  ${RED}📁 GLOBAL: ~/.claude/${NC}"
    else
        echo -e "  📁 $PROJECT_DIR"
    fi
done

echo
echo -e "${YELLOW}⚠️  This will remove:${NC}"
echo "  • All Claudook hook files"
echo "  • Settings.json files (if they contain claudook)"
echo "  • Task orchestration data"
echo "  • Analytics and backup data"
echo "  • Control files (choices_enabled, tests_enabled, etc.)"

if [ "$GLOBAL_FOUND" = true ]; then
    echo
    echo -e "${RED}⚠️  WARNING: This includes the GLOBAL installation in ~/.claude/${NC}"
fi

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
echo -e "${YELLOW}Removing all Claudook installations...${NC}"

echo "$CLAUDOOK_DIRS" | while read -r dir; do
    PROJECT_DIR=$(dirname $(dirname $(dirname "$dir")))

    if [ "$PROJECT_DIR" = "$HOME" ]; then
        echo -e "${RED}Cleaning GLOBAL: ~/.claude/${NC}"
    else
        echo -e "${BLUE}Cleaning: $PROJECT_DIR${NC}"
    fi

    # Remove claudook directory
    rm -rf "$dir"
    echo "  ✓ Removed hooks/claudook/"

    # Handle settings.json carefully
    SETTINGS_FILE="$PROJECT_DIR/.claude/settings.json"
    if [ -f "$SETTINGS_FILE" ]; then
        if grep -q "claudook" "$SETTINGS_FILE" 2>/dev/null; then
            # Check if settings.json has ONLY claudook content
            if [ $(grep -v "claudook" "$SETTINGS_FILE" | grep -c '"hooks"') -eq 0 ]; then
                rm -f "$SETTINGS_FILE"
                echo "  ✓ Removed settings.json (contained only Claudook)"
            else
                # Remove only claudook entries from settings.json
                echo "  ⚠️  settings.json contains other hooks - manual cleanup needed"
                echo "     To clean manually: edit $SETTINGS_FILE and remove claudook references"
            fi
        fi
    fi

    # Remove disabled settings
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

    # Remove hooks directory if empty
    if [ -d "$PROJECT_DIR/.claude/hooks" ]; then
        if [ -z "$(ls -A "$PROJECT_DIR/.claude/hooks")" ]; then
            rmdir "$PROJECT_DIR/.claude/hooks" 2>/dev/null
        fi
    fi

    # Only remove .claude if it's NOT the global directory and is completely empty
    if [ "$PROJECT_DIR" != "$HOME" ] && [ -d "$PROJECT_DIR/.claude" ]; then
        if [ -z "$(ls -A "$PROJECT_DIR/.claude")" ]; then
            rmdir "$PROJECT_DIR/.claude" 2>/dev/null
            echo "  ✓ Removed empty .claude/"
        else
            # List what remains for user awareness
            REMAINING=$(ls -A "$PROJECT_DIR/.claude" | wc -l | tr -d ' ')
            echo "  ℹ️  .claude/ contains $REMAINING other items - preserved"
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