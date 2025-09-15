# claudook/config-reset

Reset Claudook configuration to default settings.

## Usage
```bash
node .claude/hooks/claudook/config_manager.js --reset
```

## What gets reset:
- All feature toggles return to defaults
- Custom rules are removed
- Performance settings reset to balanced
- Security level returns to standard

## Default configuration:
- Multiple Choices: Disabled
- Test Enforcement: Disabled
- Parallel Tasks: Enabled
- Security Level: Standard
- Performance: Balanced

## Note
This preserves your hooks and commands but resets their configuration. Use with caution as custom settings will be lost.