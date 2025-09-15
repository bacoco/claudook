#!/bin/bash
set -e

# Colors for beautiful output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
cat << "EOF"
   ______ _                 _        _    _             _
  / _____| |               | |      | |  | |           | |
 | |     | | __ _ _   _  __| | ___  | |__| | ___   ___ | | __
 | |     | |/ _` | | | |/ _` |/ _ \ |  __  |/ _ \ / _ \| |/ /
 | |_____| | (_| | |_| | (_| |  __/ | |  | | (_) | (_) |   <
  \______|_|\__,_|\__,_|\__,_|\___| |_|  |_|\___/ \___/|_|\_\

   _____ _                 _             _
  / ____| |               | |           | |
 | |    | | __ _ _   _  __| | ___   ___ | | __
 | |    | |/ _` | | | |/ _` |/ _ \ / _ \| |/ /
 | |____| | (_| | |_| | (_| | (_) | (_) |   <
  \_____|_|\__,_|\__,_|\__,_|\___/ \___/|_|\_\
EOF
echo -e "${NC}"

echo -e "${PURPLE}🚀 Installing Claudook Enhancement System...${NC}"
echo "=============================================="

# Check if Claude CLI is installed
if ! command -v claude &> /dev/null; then
    echo -e "${RED}❌ Claude CLI not found.${NC}"
    echo -e "${YELLOW}Please install it first:${NC}"
    echo -e "${CYAN}npm install -g @anthropic-ai/claude-code${NC}"
    echo ""
    echo -e "${BLUE}For more info: https://docs.anthropic.com/en/docs/claude-code${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Claude CLI detected${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 required but not found${NC}"
    echo -e "${YELLOW}Please install Python 3.6+ first${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 detected${NC}"

# Determine if we're running from the repo or from curl/remote
REPO_DIR=""
TEMP_DIR=""

# Check if we're in the claudook repo
if [ -f "$(dirname "${BASH_SOURCE[0]}")/.claude/hooks/claudook/smart_controller.py" ]; then
    REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    echo -e "${GREEN}✅ Using local repository files${NC}"
# Check if script was downloaded to a specific location
elif [ -f "${HOME}/.claudook-temp/.claude/hooks/claudook/smart_controller.py" ]; then
    REPO_DIR="${HOME}/.claudook-temp"
    echo -e "${GREEN}✅ Using cached files${NC}"
else
    # Download from GitHub
    echo -e "${BLUE}📥 Downloading Claudook from GitHub...${NC}"
    TEMP_DIR=$(mktemp -d)

    # Download method 1: Try using git (fastest)
    if command -v git &> /dev/null; then
        git clone --quiet --depth 1 https://github.com/bacoco/claudook "$TEMP_DIR" 2>/dev/null || {
            echo -e "${YELLOW}Git clone failed, trying alternative method...${NC}"
            TEMP_DIR=""
        }
    fi

    # Download method 2: Use curl/wget to download archive
    if [ -z "$TEMP_DIR" ] || [ ! -d "$TEMP_DIR/.claude" ]; then
        TEMP_DIR=$(mktemp -d)
        if command -v curl &> /dev/null; then
            curl -fsSL https://github.com/bacoco/claudook/archive/main.tar.gz | tar -xz -C "$TEMP_DIR" --strip-components=1
        elif command -v wget &> /dev/null; then
            wget -qO- https://github.com/bacoco/claudook/archive/main.tar.gz | tar -xz -C "$TEMP_DIR" --strip-components=1
        else
            echo -e "${RED}❌ Neither git, curl, nor wget found. Please install one.${NC}"
            exit 1
        fi
    fi

    REPO_DIR="$TEMP_DIR"
fi

# Verify required files exist
if [ ! -f "$REPO_DIR/.claude/hooks/claudook/smart_controller.py" ]; then
    echo -e "${RED}❌ Required hook files not found. Installation aborted.${NC}"
    [ -n "$TEMP_DIR" ] && rm -rf "$TEMP_DIR"
    exit 1
fi

# Create directories
echo -e "${BLUE}📁 Creating directories...${NC}"
mkdir -p ~/.claude/hooks/claudook
mkdir -p ~/.claude/commands

# Copy ONLY the necessary files (not docs, tests, etc.)
echo -e "${BLUE}🔧 Installing hooks...${NC}"
cp "$REPO_DIR"/.claude/hooks/claudook/*.py ~/.claude/hooks/claudook/ 2>/dev/null || {
    echo -e "${RED}❌ Failed to copy hook files${NC}"
    [ -n "$TEMP_DIR" ] && rm -rf "$TEMP_DIR"
    exit 1
}
chmod +x ~/.claude/hooks/claudook/*.py

# Copy command files
echo -e "${BLUE}⚡ Installing slash commands...${NC}"
cp "$REPO_DIR"/.claude/commands/*.md ~/.claude/commands/ 2>/dev/null || {
    echo -e "${YELLOW}⚠️ Commands not found, creating basic ones...${NC}"
}

# Backup existing settings if they exist
if [ -f ~/.claude/settings.json ]; then
    echo -e "${YELLOW}💾 Backing up existing settings...${NC}"
    cp ~/.claude/settings.json ~/.claude/settings.json.backup.$(date +%s)
    echo -e "${GREEN}✅ Backup created${NC}"
fi

# Merge settings
echo -e "${BLUE}⚙️ Configuring Claude settings...${NC}"

# Check if settings-hook.json exists in repo
if [ -f "$REPO_DIR/.claude/settings-hook.json" ]; then
    if [ -f ~/.claude/settings.json ]; then
        echo -e "${BLUE}🔄 Merging with existing settings...${NC}"
        python3 << EOF
import json
import os

# Load existing settings
try:
    with open(os.path.expanduser('~/.claude/settings.json'), 'r') as f:
        existing = json.load(f)
except:
    existing = {}

# Load new hooks configuration
with open('$REPO_DIR/.claude/settings-hook.json', 'r') as f:
    new_config = json.load(f)

# Ensure hooks key exists
if 'hooks' not in existing:
    existing['hooks'] = {}

# Add our hooks without overriding existing ones
for event, hooks in new_config.get('hooks', {}).items():
    if event not in existing['hooks']:
        existing['hooks'][event] = hooks
    else:
        # Check if claudook already exists to avoid duplicates
        existing_str = str(existing['hooks'][event])
        if 'claudook' not in existing_str:
            if isinstance(existing['hooks'][event], list):
                existing['hooks'][event].extend(hooks)
            else:
                existing['hooks'][event] = [existing['hooks'][event]] + hooks

# Write back
with open(os.path.expanduser('~/.claude/settings.json'), 'w') as f:
    json.dump(existing, f, indent=2)

print('✅ Settings merged successfully')
EOF
    else
        echo -e "${BLUE}📝 Creating new settings file...${NC}"
        cp "$REPO_DIR/.claude/settings-hook.json" ~/.claude/settings.json
    fi
else
    echo -e "${YELLOW}⚠️ Settings file not found in repo${NC}"
fi

# Enable features by default
echo -e "${BLUE}🎯 Enabling default features...${NC}"
touch ~/.claude/choices_enabled
touch ~/.claude/tests_enabled

# Clean up temp directory if used
if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
    echo -e "${BLUE}🧹 Cleaning up temporary files...${NC}"
    rm -rf "$TEMP_DIR"
fi

# Test installation
echo -e "${BLUE}🧪 Testing installation...${NC}"
if python3 ~/.claude/hooks/claudook/toggle_controls.py status > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Installation test passed${NC}"
else
    echo -e "${YELLOW}⚠️ Installation test had issues, but continuing...${NC}"
fi

# Installation complete
echo ""
echo -e "${GREEN}🎉 Installation Complete!${NC}"
echo "=============================="
echo ""
echo -e "${BLUE}🎯 Available Commands:${NC}"
echo "  ${YELLOW}/status${NC}           - Check current status"
echo "  ${YELLOW}/enable-choices${NC}   - Turn on A/B/C options"
echo "  ${YELLOW}/disable-choices${NC}  - Turn off A/B/C options"
echo "  ${YELLOW}/enable-tests${NC}     - Turn on mandatory testing"
echo "  ${YELLOW}/disable-tests${NC}    - Turn off mandatory testing"
echo ""
echo -e "${BLUE}📊 Features Enabled:${NC}"
echo "  ✅ Multiple Choice System (A/B/C options)"
echo "  ✅ Automatic Testing Enforcement"
echo "  ✅ Security Guards"
echo "  ✅ Performance Optimization"
echo "  ✅ Documentation Enforcement"
echo ""
echo -e "${RED}⚠️  IMPORTANT: You must restart Claude CLI for changes to take effect!${NC}"
echo -e "${YELLOW}    Please exit Claude and run 'claude' again.${NC}"
echo ""
echo -e "${PURPLE}✨ Claudook enhancement system activated!${NC}"
echo ""
echo -e "${CYAN}Quick test after restart:${NC}"
echo "  1. Exit Claude (type 'exit' or Ctrl+C)"
echo "  2. Run 'claude' again"
echo "  3. Type '/status' to verify installation"
echo ""