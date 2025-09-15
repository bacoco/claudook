# Enable Automatic Tests

Activate mandatory test creation and execution after all code modifications.

```bash
python3 .claude/hooks/claudook/toggle_controls.py enable-tests
```

When enabled, Claude will be blocked after every code change until it creates comprehensive tests and ensures they all pass. This enforces 100% test coverage and code quality.
