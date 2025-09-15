# claudook/uninstall

Remove Claudook from the current project.

## Usage
```bash
node .claude/hooks/claudook/uninstall.js
```

## What gets removed:
- All Claudook hooks from .claude/hooks/claudook/
- All Claudook commands from .claude/commands/claudook/
- Claudook configuration files
- Claudook cache and temporary files

## What is preserved:
- Your original .claude/ directory structure
- Non-Claudook hooks and commands
- Your code and project files

## Options:
- `--keep-config` - Preserve configuration for reinstallation
- `--global` - Remove global Claudook installation (if present)

## Confirmation:
The uninstall process will ask for confirmation before removing files.