# claudook/security-enable

Enable advanced security features including pre-tool security scanning.

## Usage
```bash
cp .claude/settings-advanced.json .claude/settings.json
```

**Note**: This adds the Security Guard hook which blocks potentially dangerous commands before execution.

## What it enables:
- **Security Guard**: Blocks dangerous commands before execution
- **Git Backup**: Suggests backups before risky operations
- **Analytics Tracker**: Tracks usage patterns
- **Performance Optimizer**: Auto-optimizes code after changes
- **Documentation Enforcer**: Ensures docs are updated
- **Task Orchestrator**: Advanced parallel task execution

## Warning
These features add security and automation but may:
- Block some legitimate commands
- Slow down operations slightly
- Require more interaction for confirmations

## To disable:
Use `/claudook/security-disable` to return to minimal mode.

## Note
Security features are opt-in by default because they can interfere with normal workflow in subdirectories and with certain commands.