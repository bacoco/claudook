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
                                                             
   ____                                                     
  / ____|                                                   
 | (___  _   _ _ __   ___ _ __ _ __   _____      _____ _ __ ___
  \___ \| | | | '_ \ / _ \ '__| '_ \ / _ \ \ /\ / / _ \ '__/ __|
  ____) | |_| | |_) |  __/ |  | |_) | (_) \ V  V /  __/ |  \__ \
 |_____/ \__,_| .__/ \___|_|  | .__/ \___/ \_/\_/ \___|_|  |___/
              | |            | |                               
              |_|            |_|                               
EOF
echo -e "${NC}"

echo -e "${PURPLE}🚀 Installing Claude Hook Superpowers...${NC}"
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

# Check if jq is available (helpful but not required)
if command -v jq &> /dev/null; then
    echo -e "${GREEN}✅ jq detected (JSON processing will be faster)${NC}"
else
    echo -e "${YELLOW}💡 Consider installing jq for better JSON processing${NC}"
fi

# Get repo directory or download if not available
REPO_DIR=""
if [ -f "$(dirname "${BASH_SOURCE[0]}")/hooks/smart_controller.py" ]; then
    REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    echo -e "${GREEN}✅ Using local repository files${NC}"
else
    echo -e "${BLUE}📥 Downloading latest files from GitHub...${NC}"
    TEMP_DIR=$(mktemp -d)
    if command -v curl &> /dev/null; then
        curl -fsSL https://github.com/bacoco/claude-hook/archive/main.tar.gz | tar -xz -C "$TEMP_DIR"
        REPO_DIR="$TEMP_DIR/claude-hook-main"
    elif command -v wget &> /dev/null; then
        wget -qO- https://github.com/bacoco/claude-hook/archive/main.tar.gz | tar -xz -C "$TEMP_DIR"
        REPO_DIR="$TEMP_DIR/claude-hook-main"
    else
        echo -e "${RED}❌ Neither curl nor wget found. Please install one of them.${NC}"
        exit 1
    fi
fi

# Verify required files exist
if [ ! -f "$REPO_DIR/hooks/smart_controller.py" ]; then
    echo -e "${RED}❌ Required hook files not found. Installation aborted.${NC}"
    exit 1
fi

# Create directories
echo -e "${BLUE}📁 Creating directories...${NC}"
mkdir -p ~/.claude/hooks ~/.claude/commands ~/.claude/analytics ~/.claude/backups

# Copy hooks
echo -e "${BLUE}🔧 Installing hooks...${NC}"
cp -r "$REPO_DIR/hooks/"* ~/.claude/hooks/ 2>/dev/null || {
    echo -e "${RED}❌ Failed to copy hook files${NC}"
    exit 1
}
chmod +x ~/.claude/hooks/*.py

# Copy commands  
echo -e "${BLUE}⚡ Installing slash commands...${NC}"
cp -r "$REPO_DIR/commands/"* ~/.claude/commands/ 2>/dev/null || {
    echo -e "${YELLOW}⚠️ Slash commands not found, creating basic ones...${NC}"
    mkdir -p ~/.claude/commands
    
    # Create basic commands if not found
    cat > ~/.claude/commands/status.md << 'EOF'
# Hooks Status

Check the current status of all Claude CLI automation hooks.

```bash
python3 ~/.claude/hooks/toggle_controls.py status
```
EOF
    
    cat > ~/.claude/commands/enable-choices.md << 'EOF'
# Enable Multiple Choices

Activate the automatic A/B/C option system for complex questions.

```bash
python3 ~/.claude/hooks/toggle_controls.py enable-choices
```
EOF

    cat > ~/.claude/commands/disable-choices.md << 'EOF'
# Disable Multiple Choices

Deactivate the automatic A/B/C option system.

```bash
python3 ~/.claude/hooks/toggle_controls.py disable-choices
```
EOF

    cat > ~/.claude/commands/enable-tests.md << 'EOF'
# Enable Automatic Tests

Activate mandatory test creation and execution after all code modifications.

```bash
python3 ~/.claude/hooks/toggle_controls.py enable-tests
```
EOF

    cat > ~/.claude/commands/disable-tests.md << 'EOF'
# Disable Automatic Tests

Deactivate the mandatory test enforcement system.

```bash
python3 ~/.claude/hooks/toggle_controls.py disable-tests
```
EOF
}

# Setup configuration
echo -e "${BLUE}⚙️ Setting up configuration...${NC}"

# Backup existing settings if they exist
if [ -f ~/.claude/settings.json ]; then
    echo -e "${YELLOW}💾 Backing up existing settings...${NC}"
    cp ~/.claude/settings.json ~/.claude/settings.json.backup.$(date +%s)
    echo -e "${GREEN}✅ Backup created${NC}"
fi

# Create or merge configuration
if [ -f "$REPO_DIR/config/settings.json" ]; then
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
with open('$REPO_DIR/config/settings.json', 'r') as f:
    new_config = json.load(f)

# Merge hooks intelligently
if 'hooks' not in existing:
    existing['hooks'] = {}

# Add our hooks without overriding existing ones
for event, hooks in new_config['hooks'].items():
    if event not in existing['hooks']:
        existing['hooks'][event] = hooks
    else:
        print(f"Note: Existing {event} hooks found, adding to them...")
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
        cp "$REPO_DIR/config/settings.json" ~/.claude/settings.json
    fi
else
    # Create basic settings file if config not found
    echo -e "${YELLOW}⚠️ Config file not found, creating basic one...${NC}"
    cat > ~/.claude/settings.json << 'EOF'
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/smart_controller.py session-start"
          },
          {
            "type": "command", 
            "command": "python3 ~/.claude/hooks/smart_context.py"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/security_guard.py"
          },
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/git_backup.py"  
          },
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/analytics_tracker.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command", 
            "command": "python3 ~/.claude/hooks/smart_controller.py post-tool"
          },
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/perf_optimizer.py"
          },
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/doc_enforcer.py"
          }
        ]
      }
    ]
  }
}
EOF
fi

# Enable features by default  
echo -e "${BLUE}🎯 Enabling default features...${NC}"
touch ~/.claude/choices_enabled
touch ~/.claude/tests_enabled

# Test installation
echo -e "${BLUE}🧪 Testing installation...${NC}"
if python3 ~/.claude/hooks/toggle_controls.py status > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Installation test passed${NC}"
else
    echo -e "${YELLOW}⚠️ Installation test had issues, but continuing...${NC}"
fi

# Cleanup temp directory if used
if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
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
echo -e "${BLUE}🚀 Quick Start:${NC}"
echo "  1. ${YELLOW}claude${NC}                 - Start Claude CLI"
echo "  2. ${YELLOW}/status${NC}               - Check your superpowers"
echo "  3. Ask a complex question and see A/B/C options!"
echo ""
echo -e "${BLUE}📊 Features Enabled by Default:${NC}"
echo "  ✅ Multiple Choice System (A/B/C options)"
echo "  ✅ Automatic Testing Enforcement"
echo "  ✅ Security Guards"
echo "  ✅ Performance Optimization"  
echo "  ✅ Documentation Enforcement"
echo "  ✅ Git Backup Suggestions"
echo "  ✅ Usage Analytics"
echo ""
echo -e "${PURPLE}🦸‍♀️ Your Claude CLI now has superpowers!${NC}"

# Optional: Show quick demo
echo ""
read -p "Would you like to see a quick demo? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}🎬 Quick Demo Preview:${NC}"
    echo ""
    echo -e "${YELLOW}User:${NC} 'How should I implement caching in this API?'"
    echo ""
    echo -e "${GREEN}Claude:${NC}"
    echo "**Option A:** Simple in-memory cache (Redis/Memcached)"
    echo "**Option B:** Multi-layer cache (memory + database + CDN)"  
    echo "**Option C:** Advanced distributed cache with invalidation strategies"
    echo ""
    echo "Which approach fits your requirements? (A/B/C)"
    echo ""
    echo -e "${CYAN}[After implementation]${NC}"
    echo -e "${BLUE}🧪 TESTS REQUIRED - Creating unit and integration tests...${NC}"
    echo -e "${BLUE}🎨 AUTO-FORMATTING - Applying code style and linting...${NC}"
    echo -e "${BLUE}📚 DOCS REQUIRED - Adding comprehensive documentation...${NC}"
    echo -e "${GREEN}✅ All tests pass! Cache implementation is ready.${NC}"
    echo ""
    echo -e "${BLUE}✨ This automation happens after every code change!${NC}"
fi

echo ""
echo -e "${GREEN}Ready to revolutionize your development workflow! 🚀${NC}"
echo -e "${BLUE}Star the repo: ${CYAN}https://github.com/bacoco/claude-hook${NC}"
