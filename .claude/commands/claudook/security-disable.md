# claudook/security-disable

Disable advanced security features and return to minimal mode.

## Usage
```bash
cp .claude/settings-hook.json .claude/settings.json
```

## What it disables:
- Security Guard (pre-tool command blocking)
- Git Backup suggestions
- Analytics tracking
- Performance optimization
- Documentation enforcement
- Task orchestration

## What remains active:
- Session start context display
- A/B/C choices (if enabled)
- Test enforcement (if enabled)
- Basic Claudook functionality

## Why disable?
Advanced features can cause issues:
- Block legitimate commands
- Fail in subdirectories
- Interfere with complex workflows
- Add overhead to every operation

## To re-enable:
Use `/claudook/security-enable` when needed.