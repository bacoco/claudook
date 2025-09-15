#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Claudook Installation Verification${NC}"
echo "=========================================="

ERRORS=0
WARNINGS=0

# 1. Check if hooks directory exists
echo -e "\n${BLUE}Checking hook files...${NC}"
if [ -d ~/.claude/hooks/claudook ]; then
    echo -e "${GREEN}✅ Hook directory exists${NC}"

    # Count hook files
    HOOK_COUNT=$(ls ~/.claude/hooks/claudook/*.py 2>/dev/null | wc -l)
    if [ "$HOOK_COUNT" -eq 8 ]; then
        echo -e "${GREEN}✅ All 8 hook files present${NC}"
    else
        echo -e "${RED}❌ Expected 8 hook files, found $HOOK_COUNT${NC}"
        ERRORS=$((ERRORS + 1))
    fi

    # Check if executable
    NON_EXEC=$(find ~/.claude/hooks/claudook -name "*.py" ! -perm -u+x | wc -l)
    if [ "$NON_EXEC" -eq 0 ]; then
        echo -e "${GREEN}✅ All hooks are executable${NC}"
    else
        echo -e "${YELLOW}⚠️ $NON_EXEC hooks are not executable${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "${RED}❌ Hook directory not found${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 2. Check commands
echo -e "\n${BLUE}Checking command files...${NC}"
if [ -d ~/.claude/commands ]; then
    COMMANDS="status enable-choices disable-choices enable-tests disable-tests"
    for cmd in $COMMANDS; do
        if [ -f ~/.claude/commands/$cmd.md ]; then
            echo -e "${GREEN}✅ Command /$cmd found${NC}"
        else
            echo -e "${RED}❌ Command /$cmd missing${NC}"
            ERRORS=$((ERRORS + 1))
        fi
    done
else
    echo -e "${YELLOW}⚠️ Commands directory not found${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# 3. Check settings.json integration
echo -e "\n${BLUE}Checking settings integration...${NC}"
if [ -f ~/.claude/settings.json ]; then
    if grep -q "claudook" ~/.claude/settings.json; then
        HOOK_COUNT=$(grep -c "claudook" ~/.claude/settings.json)
        echo -e "${GREEN}✅ Settings.json contains $HOOK_COUNT claudook references${NC}"
    else
        echo -e "${RED}❌ No claudook references in settings.json${NC}"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${RED}❌ settings.json not found${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 4. Check feature toggles
echo -e "\n${BLUE}Checking feature toggles...${NC}"
if [ -f ~/.claude/choices_enabled ]; then
    echo -e "${GREEN}✅ Multiple choices ENABLED${NC}"
else
    echo -e "${YELLOW}⚠️ Multiple choices DISABLED${NC}"
fi

if [ -f ~/.claude/tests_enabled ]; then
    echo -e "${GREEN}✅ Test enforcement ENABLED${NC}"
else
    echo -e "${YELLOW}⚠️ Test enforcement DISABLED${NC}"
fi

# 5. Test toggle controls
echo -e "\n${BLUE}Testing toggle controls...${NC}"
if python3 ~/.claude/hooks/claudook/toggle_controls.py status > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Toggle controls working${NC}"
else
    echo -e "${RED}❌ Toggle controls failed${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 6. Test security guard
echo -e "\n${BLUE}Testing security guard...${NC}"
# Test safe command (should pass)
echo '{"tool_name": "Bash", "tool_input": {"command": "ls"}}' | \
    python3 ~/.claude/hooks/claudook/security_guard.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Security guard allows safe commands${NC}"
else
    echo -e "${RED}❌ Security guard blocked safe command${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Test dangerous command (should fail)
echo '{"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}' | \
    python3 ~/.claude/hooks/claudook/security_guard.py > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${GREEN}✅ Security guard blocks dangerous commands${NC}"
else
    echo -e "${RED}❌ Security guard didn't block dangerous command${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 7. Test smart controller
echo -e "\n${BLUE}Testing smart controller...${NC}"
OUTPUT=$(python3 ~/.claude/hooks/claudook/smart_controller.py session-start 2>/dev/null)
if echo "$OUTPUT" | grep -q "hookSpecificOutput"; then
    echo -e "${GREEN}✅ Smart controller returns proper JSON${NC}"
else
    echo -e "${RED}❌ Smart controller JSON format incorrect${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Summary
echo -e "\n${BLUE}=========================================${NC}"
echo -e "${BLUE}Verification Summary:${NC}"

if [ $ERRORS -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}🎉 Perfect! All checks passed.${NC}"
        echo -e "${GREEN}Claudook is fully installed and operational!${NC}"
    else
        echo -e "${GREEN}✅ Installation successful with $WARNINGS warnings.${NC}"
        echo -e "${YELLOW}Some optional features may need attention.${NC}"
    fi
else
    echo -e "${RED}❌ Installation has $ERRORS errors and $WARNINGS warnings.${NC}"
    echo -e "${RED}Please run the installer again or check the troubleshooting guide.${NC}"
    exit 1
fi

echo -e "\n${BLUE}Try these commands in Claude CLI:${NC}"
echo "  /status           - Check hook status"
echo "  /enable-choices   - Enable A/B/C options"
echo "  /enable-tests     - Enable test enforcement"

exit 0