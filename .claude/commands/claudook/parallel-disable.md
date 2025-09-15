# Disable Parallel Task Execution

Deactivate the parallel task orchestration system and return to sequential execution.

```bash
node .claude/hooks/claudook/toggle_controls.js disable-parallel
```

When disabled, Claude will process requests normally without task decomposition or parallel execution.