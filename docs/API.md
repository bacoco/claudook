# Claude Hook API Reference

Complete technical reference for Claude Hook's API and hook system.

## Hook Event Types

Claude Hook responds to the following Claude CLI events:

### SessionStart
Triggered when a new Claude CLI session begins.

**Input**: None

**Expected Output**:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "string"
  }
}
```

### PreToolUse
Triggered before any tool is executed.

**Input**:
```json
{
  "tool_name": "string",
  "tool_input": {
    "command": "string (for Bash)",
    "file_path": "string (for Edit/Write)",
    "content": "string (for Write)",
    "old_string": "string (for Edit)",
    "new_string": "string (for Edit)"
  }
}
```

**Expected Output**:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "shouldBlock": false,
    "blockingMessage": "string (if blocking)",
    "suggestion": "string (optional)"
  }
}
```

### PostToolUse
Triggered after a tool completes execution.

**Input**:
```json
{
  "tool_name": "string",
  "tool_input": {},
  "tool_output": "string"
}
```

**Expected Output**:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "string",
    "requirementMessage": "string (optional)"
  }
}
```

### UserPromptSubmit
Triggered when the user submits a prompt.

**Input**:
```json
{
  "prompt": "string"
}
```

**Expected Output**:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "string"
  }
}
```

## Hook Configuration Structure

### settings.json Schema

```json
{
  "hooks": {
    "SessionStart": [
      {
        "description": "string",
        "hooks": [
          {
            "type": "command",
            "command": "string",
            "timeout": 5000
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "description": "string",
        "toolMatcher": "regex",
        "hooks": [
          {
            "type": "command",
            "command": "string",
            "timeout": 5000
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "description": "string",
        "toolMatcher": "regex",
        "hooks": [
          {
            "type": "command",
            "command": "string",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

## Core Hook Scripts

### smart_controller.py

Main orchestrator for hook logic.

**Functions**:
```python
def handle_session_start() -> dict
    """Initialize session with context and settings"""

def handle_post_tool(data: dict) -> dict
    """Process post-tool events for test enforcement"""

def handle_slash_command(command: str) -> dict
    """Process custom slash commands"""
```

**Environment Variables**:
- `CLAUDE_CHOICES_ENABLED`: Enable/disable choice system
- `CLAUDE_TESTS_ENABLED`: Enable/disable test enforcement

### security_guard.py

Security enforcement for dangerous operations.

**Functions**:
```python
def check_dangerous_command(command: str) -> tuple[bool, str]
    """Check if command is dangerous"""

def check_sensitive_file(file_path: str) -> tuple[bool, str]
    """Check if file is sensitive"""

def analyze_security_risk(tool_name: str, tool_input: dict) -> dict
    """Analyze overall security risk"""
```

**Configuration**:
```python
dangerous_patterns = [
    (r'pattern', 'description'),
    # Add custom patterns
]

sensitive_patterns = [
    '.env',
    '.ssh/',
    # Add custom patterns
]
```

### perf_optimizer.py

Code optimization and formatting.

**Functions**:
```python
def suggest_optimizations(file_path: str) -> list[str]
    """Generate optimization suggestions"""

def get_formatter_command(extension: str) -> str
    """Get appropriate formatter for file type"""
```

**Tool Mapping**:
```python
tools_map = {
    '.py': {
        'formatter': 'black',
        'linter': 'flake8',
        'import_sorter': 'isort'
    },
    '.js': {
        'formatter': 'prettier',
        'linter': 'eslint'
    }
    # Add more mappings
}
```

### doc_enforcer.py

Documentation requirement enforcement.

**Functions**:
```python
def check_documentation(file_path: str, content: str) -> list[str]
    """Check documentation requirements"""

def generate_doc_requirements(language: str) -> list[str]
    """Generate documentation requirements by language"""
```

### analytics_tracker.py

Usage analytics and tracking.

**Functions**:
```python
def track_event(event: dict) -> None
    """Track usage event"""

def get_daily_stats() -> dict
    """Get daily usage statistics"""

def cleanup_old_files() -> None
    """Clean up old analytics files"""
```

**Data Structure**:
```python
{
    "timestamp": "ISO-8601",
    "event_type": "string",
    "tool_name": "string",
    "file_path": "string",
    "language": "string",
    "project": "string"
}
```

### git_backup.py

Git integration for backup suggestions.

**Functions**:
```python
def suggest_backup(file_path: str) -> str
    """Generate backup suggestion"""

def get_git_status() -> dict
    """Get current git status"""

def create_backup_branch(branch_name: str) -> bool
    """Create backup branch"""
```

### toggle_controls.py

Feature toggle management.

**Functions**:
```python
def enable_feature(feature: str) -> None
    """Enable a feature"""

def disable_feature(feature: str) -> None
    """Disable a feature"""

def get_status() -> dict
    """Get current feature status"""
```

**Commands**:
- `enable-choices`: Enable multiple choice system
- `disable-choices`: Disable multiple choice system
- `enable-tests`: Enable test enforcement
- `disable-tests`: Disable test enforcement
- `status`: Get current status

## Custom Hook Development

### Basic Hook Template

```python
#!/usr/bin/env python3
import json
import sys
import os

def main():
    # Read input from stdin
    if not sys.stdin.isatty():
        data = json.loads(sys.stdin.read())
    else:
        data = {}

    # Get event type from command line
    event_type = sys.argv[1] if len(sys.argv) > 1 else 'unknown'

    # Process based on event type
    if event_type == 'session-start':
        output = handle_session_start()
    elif event_type == 'pre-tool':
        output = handle_pre_tool(data)
    elif event_type == 'post-tool':
        output = handle_post_tool(data)
    else:
        output = {}

    # Output JSON response
    print(json.dumps(output))

def handle_session_start():
    return {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "Your custom context"
        }
    }

def handle_pre_tool(data):
    # Your pre-tool logic
    return {}

def handle_post_tool(data):
    # Your post-tool logic
    return {}

if __name__ == "__main__":
    main()
```

### Error Handling

Always include proper error handling:

```python
try:
    # Your hook logic
    result = process_hook(data)
    print(json.dumps(result))
except Exception as e:
    # Log error but don't break Claude CLI
    if os.environ.get('CLAUDE_HOOK_DEBUG'):
        print(f"Error: {e}", file=sys.stderr)
    print("{}")  # Return empty JSON
    sys.exit(0)
```

### Testing Hooks

Test hooks individually:

```bash
# Test with no input
python3 your_hook.py session-start

# Test with input
echo '{"tool_name":"Edit","tool_input":{"file_path":"test.py"}}' | \
python3 your_hook.py post-tool

# Test with debug output
CLAUDE_HOOK_DEBUG=true python3 your_hook.py session-start
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CLAUDOOK_DEBUG` | Enable debug output | `false` |
| `CLAUDOOK_VERBOSE` | Enable verbose logging | `false` |
| `CLAUDE_CHOICES_ENABLED` | Enable choice system | `true` |
| `CLAUDE_TESTS_ENABLED` | Enable test enforcement | `true` |
| `CLAUDE_SECURITY_LEVEL` | Security level (strict/normal/permissive) | `normal` |
| `CLAUDE_ANALYTICS_ENABLED` | Enable analytics tracking | `true` |
| `CLAUDE_ANALYTICS_RETENTION_DAYS` | Days to retain analytics | `30` |

## File System Structure

```
~/.claude/
├── settings.json           # Main configuration
├── choices_enabled         # Feature flag file
├── tests_enabled          # Feature flag file
├── hooks/                 # Hook scripts
│   ├── smart_controller.py
│   ├── security_guard.py
│   ├── perf_optimizer.py
│   ├── doc_enforcer.py
│   ├── analytics_tracker.py
│   ├── git_backup.py
│   └── toggle_controls.py
├── commands/              # Slash commands
│   ├── enable-choices.md
│   ├── disable-choices.md
│   ├── enable-tests.md
│   ├── disable-tests.md
│   └── status.md
└── analytics/             # Analytics data
    ├── daily_YYYY-MM-DD.json
    └── events.jsonl
```

## Hook Communication Protocol

### Input/Output Flow

1. Claude CLI triggers event
2. Hook script receives JSON via stdin
3. Hook processes data
4. Hook outputs JSON to stdout
5. Claude CLI processes hook response

### Blocking Operations

For PreToolUse hooks to block an operation:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "shouldBlock": true,
    "blockingMessage": "Operation blocked: Reason"
  }
}
```

### Adding Context

For SessionStart and PostToolUse to add context:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Additional instructions or context for Claude"
  }
}
```

## Performance Considerations

### Timeout Handling

All hooks should complete within 5 seconds:

```python
import signal

def timeout_handler(signum, frame):
    print("{}")
    sys.exit(0)

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(5)  # 5 second timeout
```

### Caching

Cache expensive operations:

```python
_cache = {}

def expensive_operation(key):
    if key not in _cache:
        _cache[key] = compute_expensive_value(key)
    return _cache[key]
```

### Early Exit

Exit early when possible:

```python
def handle_hook(data):
    # Quick checks first
    if not should_process(data):
        return {}

    # Expensive operations only if needed
    return process_data(data)
```

## Security Best Practices

1. **Never execute user input directly**
2. **Validate all input data**
3. **Use subprocess with shell=False when possible**
4. **Sanitize file paths**
5. **Don't store sensitive data in hooks**
6. **Use environment variables for secrets**

## Debugging

### Enable Debug Mode

```bash
export CLAUDE_HOOK_DEBUG=true
export CLAUDE_HOOK_VERBOSE=true
```

### Debug Output

```python
def debug_log(message):
    if os.environ.get('CLAUDE_HOOK_DEBUG'):
        print(f"DEBUG: {message}", file=sys.stderr)
```

### Common Issues

1. **JSON parsing errors**: Validate JSON output
2. **Permission issues**: Ensure scripts are executable
3. **Import errors**: Use system Python, not virtualenv
4. **Timeout issues**: Optimize or increase timeout
5. **Path issues**: Use absolute paths

## Version Compatibility

| Claude Hook Version | Claude CLI Version | Python Version |
|--------------------|--------------------|----------------|
| 1.0.0+             | 0.1.0+             | 3.6+           |

## Contributing

To add new hooks or features:

1. Fork the repository
2. Create your hook following the template
3. Add tests for your hook
4. Update documentation
5. Submit a pull request

## Support

- GitHub Issues: [github.com/bacoco/claude-hook/issues](https://github.com/bacoco/claude-hook/issues)
- Discussions: [github.com/bacoco/claude-hook/discussions](https://github.com/bacoco/claude-hook/discussions)
- Documentation: [github.com/bacoco/claude-hook/docs](https://github.com/bacoco/claude-hook/docs)

---

*Claude Hook API v1.0.0 - Last updated: 2024*