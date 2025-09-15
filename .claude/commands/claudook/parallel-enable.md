# Enable Parallel Task Execution

Activate the parallel task orchestration system that decomposes complex requests into parallelizable subtasks.

```bash
node .claude/hooks/claudook/toggle_controls.js enable-parallel
```

This enables:
- Automatic task decomposition
- Dependency analysis and DAG creation
- Parallel execution of independent tasks
- Specialized agent spawning
- Progress tracking and visualization