# Disable Parallel Task Execution

Deactivate the parallel task orchestration system and return to sequential execution.

```bash
python3 .claude/hooks/claudook/toggle_controls.py disable-parallel
```

When disabled, Claude will process requests normally without task decomposition or parallel execution.