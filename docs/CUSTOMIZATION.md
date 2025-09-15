# Customization Guide

Learn how to customize Claude Hook to fit your specific workflow needs.

## Configuration Files

### Main Settings
- `~/.claude/settings.json` - Main hook configuration
- `~/.claude/choices_enabled` - Enable/disable choice system
- `~/.claude/tests_enabled` - Enable/disable test enforcement

### Hook Scripts
All hooks are located in `~/.claude/hooks/` and can be modified:
- `smart_controller.py` - Main control logic
- `security_guard.py` - Security policies  
- `perf_optimizer.py` - Code formatting rules
- `doc_enforcer.py` - Documentation requirements

## Customizing Features

### 1. Multiple Choice System

Edit the context in `smart_controller.py`:

```python
# Customize the choice prompt
context_parts.append("""
🎯 CUSTOM CHOICE MODE:
For complex questions, I'll offer:
• **Option A:** [your custom description]
• **Option B:** [your custom description] 
• **Option C:** [your custom description]
""")
```

### 2. Test Enforcement

Modify test requirements in `smart_controller.py`:

```python
# Add custom test requirements
mandatory_msg = f"""
⚠️ CUSTOM TEST REQUIREMENTS for {file_path}

Your specific testing requirements:
1. Unit tests with 90% coverage
2. Integration tests for APIs
3. Performance benchmarks
4. Security tests
"""
```

### 3. Security Rules

Add custom security patterns in `security_guard.py`:

```python
# Add your dangerous patterns
dangerous_patterns = [
    # Your custom patterns
    (r'your-dangerous-command', "Your description"),
    (r'another-pattern', "Another description"),
]

# Add sensitive file patterns
sensitive_patterns = [
    "your-sensitive-file",
    "config/secrets",
]
```

### 4. Code Optimization

Customize formatting tools in `perf_optimizer.py`:

```python
# Add your preferred formatters
tools_map = {
    '.py': {
        'formatter': 'your-python-formatter',
        'linter': 'your-linter',
        'custom_tool': 'your-custom-tool'
    },
    # Add more languages
}
```

### 5. Documentation Requirements

Modify documentation standards in `doc_enforcer.py`:

```python
# Customize documentation requirements
requirements = {
    '.py': [
        '✓ Your custom Python doc standards',
        '✓ Your team-specific requirements',
        '✓ Your quality gates',
    ]
}
```

## Project-Specific Configurations

### Per-Project Settings

Create `.claude/settings.local.json` in your project:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/custom-project-hook.py"
          }
        ]
      }
    ]
  }
}
```

### Custom Project Hook Example

```python
#!/usr/bin/env python3
# .claude/custom-project-hook.py

import json

# Project-specific context
context = f"""
PROJECT CONTEXT for {os.getcwd()}:
• Team: Your Team Name  
• Standards: Your coding standards
• Deployment: Your deployment process
• Testing: Your testing requirements
"""

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context
    }
}))
```

## Language-Specific Customization

### Python Projects

```python
# Add in smart_context.py
def get_python_custom_context():
    context = []
    if os.path.exists('pyproject.toml'):
        context.append("🐍 Modern Python project with pyproject.toml")
    if os.path.exists('.black'):
        context.append("🎨 Black formatting configured")
    if os.path.exists('pytest.ini'):
        context.append("🧪 Pytest configuration found")
    return context
```

### Node.js Projects

```python
# Add in smart_context.py  
def get_nodejs_custom_context():
    context = []
    if os.path.exists('tsconfig.json'):
        context.append("📘 TypeScript project")
    if os.path.exists('.eslintrc.js'):
        context.append("🔍 ESLint configured")
    if os.path.exists('jest.config.js'):
        context.append("🧪 Jest testing configured")
    return context
```

## Team Customization

### Shared Team Settings

Create a team configuration repository:

```bash
# team-claude-config/
├── hooks/
│   ├── team-standards.py
│   └── team-security.py
├── commands/
│   └── team-commands/
└── install-team.sh
```

### Team Installation Script

```bash
#!/bin/bash
# install-team.sh

# Install base claudook
curl -fsSL https://raw.githubusercontent.com/bacoco/claudook/main/install.sh | bash

# Add team customizations
cp team-hooks/* ~/.claude/hooks/
cp team-commands/* ~/.claude/commands/

echo "✅ Team Claudook configuration installed!"
```

## Advanced Customization

### Custom Hook Events

Create hooks for additional events:

```python
# custom-hook.py
#!/usr/bin/env python3
import json
import sys

# Your custom logic here
def handle_custom_event():
    # Process custom event
    pass

if __name__ == "__main__":
    handle_custom_event()
```

### Integration with External Tools

```python
# slack-notification.py
import requests

def notify_team(message):
    webhook_url = os.environ.get('SLACK_WEBHOOK')
    if webhook_url:
        requests.post(webhook_url, json={"text": message})
```

### Custom Analytics

```python
# custom-analytics.py
def track_custom_metrics(event):
    # Your custom tracking logic
    metrics = {
        "team_productivity": calculate_productivity(event),
        "code_quality_score": calculate_quality(event),
        "custom_metric": your_custom_calculation(event)
    }
    
    # Send to your analytics platform
    send_to_analytics_platform(metrics)
```

## Environment Variables

Set environment variables for customization:

```bash
# ~/.bashrc or ~/.zshrc
export CLAUDE_TEAM_MODE="true"
export CLAUDE_SECURITY_LEVEL="strict"
export CLAUDE_CUSTOM_CONFIG="/path/to/custom/config"
export SLACK_WEBHOOK="your-webhook-url"
```

## Testing Your Customizations

```bash
# Test hook individually
python3 ~/.claude/hooks/your-custom-hook.py

# Test with sample data
echo '{"tool_name":"Edit","tool_input":{"file_path":"test.py"}}' | python3 ~/.claude/hooks/your-hook.py

# Validate settings.json
python3 -c "import json; json.load(open('~/.claude/settings.json'))"
```

## Troubleshooting Custom Hooks

### Debug Mode

Add debug output to your hooks:

```python
import sys
import os

DEBUG = os.environ.get('CLAUDE_HOOK_DEBUG', False)

if DEBUG:
    print(f"DEBUG: Processing {data}", file=sys.stderr)
```

### Error Handling

Always include error handling:

```python
try:
    # Your hook logic
    pass
except Exception as e:
    if DEBUG:
        print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(0)  # Don't break Claude CLI
```

## Sharing Your Customizations

1. Fork the repository
2. Add your customizations
3. Create a pull request
4. Share with the community!

## Getting Help

- Open an issue on GitHub
- Join discussions
- Check existing customizations in the community
- Read the [API Reference](API.md)

---

Happy customizing! 🚀
