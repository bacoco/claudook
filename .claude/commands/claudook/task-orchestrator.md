# Task Orchestrator

Decompose complex tasks and manage GitHub task-master format todos

## Usage
```bash
node .claude/hooks/claudook/task_orchestrator.js
```

## Features
- Breaks down complex tasks into subtasks
- Creates GitHub task-master formatted todos
- Manages project-specific task lists
- Tracks dependencies between tasks
- Exports tasks for parallel execution

## Example
When handling "Build user authentication with tests", orchestrator will:
1. Create subtasks (implement auth, write tests, document)
2. Identify dependencies
3. Export as GitHub task-master format
4. Enable parallel execution where possible
