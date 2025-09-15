# claudook/config-show

Display all current Claudook configuration settings.

## Usage
```bash
node .claude/hooks/claudook/config_manager.js --show
```

## Shows:
- Active features (choices, tests, parallel execution)
- Hook configurations
- Performance settings
- Security policies
- Custom rules
- Integration settings

## Output format:
```
Claudook Configuration v1.0.0
============================
Features:
  ✅ Multiple Choices: Enabled
  ❌ Test Enforcement: Disabled
  ✅ Parallel Tasks: Enabled

Security:
  Level: Standard
  OWASP Compliance: Yes

Performance:
  Optimization: Aggressive
  Caching: Enabled
```