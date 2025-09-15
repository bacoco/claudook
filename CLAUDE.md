# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Master Claude Hook is a comprehensive automation system that enhances Claude Code with intelligent workflows and productivity features. This repository contains reusable hook scripts that can be copied to ANY project to add "superpowers" to Claude Code sessions.

## Installation Commands

### Quick Install in Any Project
```bash
# Clone and run installer
git clone https://github.com/bacoco/claude-hook /tmp/claude-hook
cd /tmp/claude-hook && ./install.sh

# Or download and install directly
curl -fsSL https://raw.githubusercontent.com/bacoco/claude-hook/main/install.sh | bash
```

### Manual Installation for Custom Setup
```bash
# 1. Copy hook files to Claude's directory
cp -r hooks/* ~/.claude/hooks/

# 2. Merge settings into Claude's configuration
python3 -c "
import json
with open('config/settings.json') as f: new = json.load(f)
with open('~/.claude/settings.json') as f: existing = json.load(f)
# Merge logic here...
"

# 3. Copy command files
cp -r commands/* ~/.claude/commands/

# 4. Enable desired features
touch ~/.claude/choices_enabled  # Enable A/B/C choices
touch ~/.claude/tests_enabled    # Enable test enforcement
```

## Feature Control Commands

### In Claude CLI Session
- `/status` - Show current hook status and enabled features
- `/enable-choices` - Enable A/B/C multiple choice system
- `/disable-choices` - Disable multiple choice system
- `/enable-tests` - Enable mandatory test enforcement
- `/disable-tests` - Disable test enforcement

### Direct Python Commands
```bash
python3 ~/.claude/hooks/toggle_controls.py status
python3 ~/.claude/hooks/toggle_controls.py enable-choices
python3 ~/.claude/hooks/toggle_controls.py enable-tests
```

## Architecture

### Core Hook System

The system uses Claude's native hook events to inject behavior:

1. **SessionStart Hook** - Injects context when session begins
   - `smart_controller.py session-start` - Adds A/B/C and test instructions
   - `smart_context.py` - Loads project-specific context

2. **PreToolUse Hook** - Validates before tool execution
   - `security_guard.py` - Blocks dangerous commands
   - `git_backup.py` - Suggests backups for critical changes
   - `analytics_tracker.py` - Records usage patterns

3. **PostToolUse Hook** - Enforces requirements after file changes
   - `smart_controller.py post-tool` - Enforces test creation
   - `perf_optimizer.py` - Auto-formats and optimizes code
   - `doc_enforcer.py` - Requires documentation

### Hook Components

**Control System** (`hooks/toggle_controls.py`):
- Manages feature toggles via control files
- `~/.claude/choices_enabled` - A/B/C system state
- `~/.claude/tests_enabled` - Test enforcement state

**Smart Controller** (`hooks/smart_controller.py`):
- Main orchestrator for choice system and test enforcement
- Injects context at session start based on enabled features
- Blocks continuation after code changes until tests pass

**Security Guard** (`hooks/security_guard.py`):
- Pattern matching for dangerous commands
- Blocks destructive operations (rm -rf /, curl | bash, etc.)
- Protects sensitive files and system resources

**Performance Optimizer** (`hooks/perf_optimizer.py`):
- Auto-formats code based on file type
- Runs linters and style checkers
- Organizes imports and cleans code

**Documentation Enforcer** (`hooks/doc_enforcer.py`):
- Detects undocumented functions
- Requires docstrings/JSDoc/comments
- Validates documentation quality

**Git Backup** (`hooks/git_backup.py`):
- Detects significant changes
- Suggests backup branch creation
- Provides rollback commands

**Analytics Tracker** (`hooks/analytics_tracker.py`):
- Records tool usage patterns
- Tracks coding time by language
- Generates productivity insights

### Configuration Structure

The system is configured via `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [...],
    "PreToolUse": [...],
    "PostToolUse": [...]
  }
}
```

Each hook entry specifies:
- `matcher` - Tool name pattern to match
- `type` - "command" for external scripts
- `command` - Python script to execute

## Implementation Guide

### To Add These Hooks to a New Project

1. **Copy the hook files**:
   ```bash
   # From this repo to target project
   cp -r hooks ~/.claude/hooks/claude-hook/
   ```

2. **Register hooks in settings**:
   - Merge `config/settings.json` into `~/.claude/settings.json`
   - Or manually add hook entries

3. **Set up commands**:
   ```bash
   cp -r commands/* ~/.claude/commands/
   ```

4. **Enable desired features**:
   ```bash
   touch ~/.claude/choices_enabled
   touch ~/.claude/tests_enabled
   ```

### Creating Custom Hooks

1. **Create Python script** in `hooks/`:
   ```python
   #!/usr/bin/env python3
   import json
   import sys

   data = json.load(sys.stdin)
   # Process hook data
   result = {"hookSpecificOutput": {...}}
   json.dump(result, sys.stdout)
   ```

2. **Register in settings.json**:
   ```json
   {
     "hooks": {
       "EventType": [{
         "matcher": "ToolName",
         "hooks": [{
           "type": "command",
           "command": "python3 ~/.claude/hooks/your_hook.py"
         }]
       }]
     }
   }
   ```

3. **Add control command** in `commands/`:
   ```markdown
   # Your Command
   Description here
   ```bash
   python3 ~/.claude/hooks/your_hook.py
   ```

## Feature Behaviors

### A/B/C Multiple Choice System
When enabled, complex questions trigger three options:
- **Option A**: Quick/simple implementation
- **Option B**: Balanced approach with trade-offs
- **Option C**: Advanced/comprehensive solution

User selects A, B, or C before implementation proceeds.

### Mandatory Test Enforcement
After code modifications:
1. Blocks further operations
2. Forces test file creation
3. Requires test execution
4. Only continues when tests pass

### Security Protection
Automatically blocks:
- Destructive file operations (`rm -rf /`)
- Dangerous network commands (`curl | bash`)
- System modifications
- Sensitive file access

### Auto-Optimization
After file edits:
- Formats code (Black, Prettier, gofmt)
- Runs linters (ESLint, flake8, etc.)
- Organizes imports
- Applies style guidelines

## Troubleshooting

### If hooks aren't triggering
1. Check `~/.claude/settings.json` has correct paths
2. Verify Python 3 is installed: `python3 --version`
3. Check hook files are executable: `chmod +x ~/.claude/hooks/*.py`
4. Test directly: `python3 ~/.claude/hooks/toggle_controls.py status`

### To disable all hooks temporarily
```bash
mv ~/.claude/settings.json ~/.claude/settings.json.backup
```

### To uninstall completely
```bash
rm -rf ~/.claude/hooks/
rm ~/.claude/choices_enabled ~/.claude/tests_enabled
# Then manually remove hook entries from settings.json
```

## Development Workflow

When developing new hooks or modifying existing ones:

1. **Test hooks locally**:
   ```bash
   echo '{"tool_name": "Bash", "tool_input": {"command": "ls"}}' | python3 hooks/security_guard.py
   ```

2. **Check hook output format**:
   - Must return valid JSON
   - Include `hookSpecificOutput` key
   - Non-zero exit blocks operation

3. **Update installation script**:
   - Add new files to copy operations
   - Update settings.json merge logic
   - Add new commands if needed

## Important Notes

- Hooks run in subprocess with stdin/stdout communication
- Exit code 0 allows operation, non-zero blocks
- Control files in `~/.claude/` persist across sessions
- All hooks are Python 3 scripts for portability
- Security guard is always active (no toggle)