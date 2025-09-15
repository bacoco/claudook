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
   ______ _                 _             _
  / _____| |               | |           | |
 | |     | | __ _ _   _  __| | ___   ___ | | __
 | |     | |/ _` | | | |/ _` |/ _ \ / _ \| |/ /
 | |_____| | (_| | |_| | (_| | (_) | (_) |   <
  \______|_|\__,_|\__,_|\__,_|\___/ \___/|_|\_\

  LOCAL INSTALLATION
EOF
echo -e "${NC}"

echo -e "${PURPLE}🚀 Installing Claudook locally in current directory...${NC}"
echo "=============================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 required but not found${NC}"
    echo -e "${YELLOW}Please install Python 3.6+ first${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 detected${NC}"

# Get the current directory
INSTALL_DIR=$(pwd)
echo -e "${BLUE}📁 Installing to: ${CYAN}$INSTALL_DIR${NC}"

# SAFETY CHECK: Prevent installation in global Claude directory
if [ "$INSTALL_DIR" = "$HOME/.claude" ] || [ "$INSTALL_DIR" = "$HOME" ]; then
    echo -e "${RED}❌ ERROR: Cannot install in global Claude directory!${NC}"
    echo -e "${YELLOW}Claudook must be installed in individual project directories.${NC}"
    echo -e "${YELLOW}Please navigate to your project directory and run the installer again.${NC}"
    exit 1
fi

# Determine source directory
REPO_DIR=""
TEMP_DIR=""

# Check if we're in the claudook repo
if [ -f "$(dirname "${BASH_SOURCE[0]}")/.claude/hooks/claudook/smart_controller.py" ]; then
    REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    echo -e "${GREEN}✅ Using local repository files${NC}"
else
    # Download from GitHub
    echo -e "${BLUE}📥 Downloading Claudook from GitHub...${NC}"
    TEMP_DIR=$(mktemp -d)

    # Download using git or curl/wget
    if command -v git &> /dev/null; then
        git clone --quiet --depth 1 https://github.com/bacoco/claudook "$TEMP_DIR" 2>/dev/null || {
            echo -e "${YELLOW}Git clone failed, trying alternative method...${NC}"
            rm -rf "$TEMP_DIR"
            TEMP_DIR=$(mktemp -d)
            if command -v curl &> /dev/null; then
                curl -fsSL https://github.com/bacoco/claudook/archive/main.tar.gz | tar -xz -C "$TEMP_DIR" --strip-components=1
            elif command -v wget &> /dev/null; then
                wget -qO- https://github.com/bacoco/claudook/archive/main.tar.gz | tar -xz -C "$TEMP_DIR" --strip-components=1
            else
                echo -e "${RED}❌ Neither git, curl, nor wget found. Please install one.${NC}"
                exit 1
            fi
        }
    else
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

# Create local .claude directories
echo -e "${BLUE}📁 Creating local .claude directories...${NC}"
mkdir -p "$INSTALL_DIR/.claude/hooks/claudook"
mkdir -p "$INSTALL_DIR/.claude/commands"

# Copy hook files
echo -e "${BLUE}🔧 Installing hooks locally...${NC}"
cp "$REPO_DIR"/.claude/hooks/claudook/*.py "$INSTALL_DIR/.claude/hooks/claudook/" 2>/dev/null || {
    echo -e "${RED}❌ Failed to copy hook files${NC}"
    [ -n "$TEMP_DIR" ] && rm -rf "$TEMP_DIR"
    exit 1
}
chmod +x "$INSTALL_DIR/.claude/hooks/claudook/"*.py

# Copy command files
echo -e "${BLUE}⚡ Installing slash commands locally...${NC}"
cp "$REPO_DIR"/.claude/commands/*.md "$INSTALL_DIR/.claude/commands/" 2>/dev/null || {
    echo -e "${YELLOW}⚠️ Commands not found, creating basic ones...${NC}"
}

# Create local settings file
echo -e "${BLUE}⚙️ Creating local settings configuration...${NC}"

# Check if local settings already exist
if [ -f "$INSTALL_DIR/.claude/settings.json" ]; then
    echo -e "${YELLOW}💾 Backing up existing local settings...${NC}"
    cp "$INSTALL_DIR/.claude/settings.json" "$INSTALL_DIR/.claude/settings.json.backup.$(date +%s)"
    echo -e "${GREEN}✅ Backup created${NC}"
fi

# Copy settings file
if [ -f "$REPO_DIR/.claude/settings-hook.json" ]; then
    echo -e "${BLUE}📝 Creating local settings file...${NC}"

    # Adjust paths in settings to be relative
    python3 << EOF
import json
import os

# Load the settings template
with open('$REPO_DIR/.claude/settings-hook.json', 'r') as f:
    settings = json.load(f)

# Update all hook commands to use local paths
if 'hooks' in settings:
    for event_type in settings['hooks']:
        for hook_group in settings['hooks'][event_type]:
            if 'hooks' in hook_group:
                for hook in hook_group['hooks']:
                    if 'command' in hook and '~/.claude/hooks/claudook/' in hook['command']:
                        # Replace global path with local path
                        hook['command'] = hook['command'].replace(
                            '~/.claude/hooks/claudook/',
                            '.claude/hooks/claudook/'
                        )

# Check if we need to merge with existing settings
existing_settings = {}
settings_path = '$INSTALL_DIR/.claude/settings.json'
if os.path.exists(settings_path):
    try:
        with open(settings_path, 'r') as f:
            existing_settings = json.load(f)
    except:
        pass

# Merge if existing settings found
if existing_settings:
    # Ensure hooks key exists
    if 'hooks' not in existing_settings:
        existing_settings['hooks'] = {}

    # Add our hooks without overriding existing ones
    for event, hooks in settings.get('hooks', {}).items():
        if event not in existing_settings['hooks']:
            existing_settings['hooks'][event] = hooks
        else:
            # Check if claudook already exists to avoid duplicates
            existing_str = str(existing_settings['hooks'][event])
            if 'claudook' not in existing_str:
                if isinstance(existing_settings['hooks'][event], list):
                    existing_settings['hooks'][event].extend(hooks)

    settings = existing_settings

# Write the settings
with open(settings_path, 'w') as f:
    json.dump(settings, f, indent=2)

print('✅ Local settings configured')
EOF
fi

# Create local feature flags
echo -e "${BLUE}🎯 Enabling default features locally...${NC}"
touch "$INSTALL_DIR/.claude/choices_enabled"
touch "$INSTALL_DIR/.claude/tests_enabled"

# Create CLAUDE.md file with local installation note
echo -e "${BLUE}📝 Creating CLAUDE.md with local configuration...${NC}"
cat > "$INSTALL_DIR/CLAUDE.md" << 'EOF'
# Claudook Configuration

This project has Claudook installed locally in the `.claude/` directory.

## Local Installation
Claudook is installed in this project's `.claude/` directory, providing project-specific enhancements without affecting global Claude settings.

## Available Commands
- `/status` - Check hook status
- `/enable-choices` - Enable A/B/C options
- `/disable-choices` - Disable A/B/C options
- `/enable-tests` - Enable test enforcement
- `/disable-tests` - Disable test enforcement

## Features
- Multiple Choice System (A/B/C options for complex tasks)
- Test Enforcement (mandatory tests for code changes)
- Security Guards (blocks dangerous operations)
- Performance Optimization (automatic code improvements)
- Documentation Enforcement (requires proper docs)

## Project-Specific Configuration
The hooks and settings are contained in:
- `.claude/hooks/claudook/` - Hook scripts
- `.claude/settings.json` - Local settings
- `.claude/commands/` - Slash commands
- `.claude/choices_enabled` - Feature flag
- `.claude/tests_enabled` - Feature flag
EOF

# Clean up temp directory if used
if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
    echo -e "${BLUE}🧹 Cleaning up temporary files...${NC}"
    rm -rf "$TEMP_DIR"
fi

# Test installation
echo -e "${BLUE}🧪 Testing local installation...${NC}"
if python3 "$INSTALL_DIR/.claude/hooks/claudook/toggle_controls.py" status > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Installation test passed${NC}"
else
    echo -e "${YELLOW}⚠️ Installation test had issues, but continuing...${NC}"
fi

# Installation complete
echo ""
echo -e "${GREEN}🎉 Local Installation Complete!${NC}"
echo "=============================="
echo ""
echo -e "${BLUE}📁 Installed in: ${CYAN}$INSTALL_DIR/.claude/${NC}"
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
echo -e "${GREEN}✨ Claudook is now active for this project!${NC}"
echo ""
echo -e "${CYAN}This is a LOCAL installation:${NC}"
echo "  • Files are in ${YELLOW}$INSTALL_DIR/.claude/${NC}"
echo "  • Settings are project-specific"
echo "  • Won't affect other Claude projects"
echo "  • Works immediately (no restart needed)"
echo ""