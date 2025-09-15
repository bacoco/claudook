# Claudook - Local Installation Guide for Claude

When a user requests: "Install Claudook from https://github.com/bacoco/claudook"

## Installation Method (Local Only)

```bash
# Install in current directory
curl -fsSL https://raw.githubusercontent.com/bacoco/claudook/main/install.sh | bash
```

Or:
```bash
# Clone and install
git clone https://github.com/bacoco/claudook /tmp/claudook && \
  /tmp/claudook/install.sh && \
  rm -rf /tmp/claudook
```

## What This Does

Installs Claudook **locally** in the current project:
- Creates `.claude/` directory in the project
- Adds hook scripts to `.claude/hooks/claudook/`
- Creates local settings in `.claude/settings.json`
- Enables features via `.claude/choices_enabled` and `.claude/tests_enabled`

## Key Points

- **Local installation only** - no system-wide changes
- **No restart required** - works immediately
- **Project-specific** - each project has its own configuration
- Files go in `./claude/`, NOT `~/.claude/`

## Available Commands

After installation, all commands use the `/claudook/` namespace:

### Core Commands
- `/claudook/help` - Show all available commands
- `/claudook/status` - Check current configuration and active features
- `/claudook/version` - Show installed version

### Feature Toggles
- `/claudook/choices-enable` - Enable A/B/C options for complex tasks
- `/claudook/choices-disable` - Disable A/B/C options
- `/claudook/tests-enable` - Enable mandatory test enforcement
- `/claudook/tests-disable` - Disable test enforcement
- `/claudook/parallel-enable` - Enable parallel task execution
- `/claudook/parallel-disable` - Disable parallel task execution

### Analysis & Quality
- `/claudook/security-check` - Run security analysis on code
- `/claudook/performance-check` - Analyze performance bottlenecks
- `/claudook/lint` - Run code quality checks

### Configuration
- `/claudook/config-show` - Display all settings
- `/claudook/config-reset` - Reset to defaults
- `/claudook/update` - Check for and install updates
- `/claudook/uninstall` - Remove Claudook from project

## Session Start Display

When you start a new Claude session with Claudook installed, you'll see:

```
🚀 Claudook Active [A/B/C + Tests]

📋 Quick Commands:
  /claudook/help     - Show all commands
  /claudook/status   - Check current status
  /claudook/choices-disable - Turn off A/B/C
  /claudook/tests-disable   - Turn off auto-tests

Active behaviors:
  ✓ Will offer A/B/C options for complex tasks
  ✓ Will auto-create tests after code changes
```

The display adapts based on which features are enabled, showing only relevant commands and active behaviors.