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

After installation:
- `/claudook/status` - Check hook status
- `/claudook/choices-enable` - Enable A/B/C options
- `/claudook/choices-disable` - Disable A/B/C options
- `/claudook/tests-enable` - Enable test enforcement
- `/claudook/tests-disable` - Disable test enforcement