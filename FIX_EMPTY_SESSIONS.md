# Fix for Empty Session Directories

## Problem
Older versions of Claudook (before v2.7.5) created empty session directories in `.claude/tasks/session_*/` without populating them with task files.

## Symptoms
- Empty directories like `/session_20250915_114345/`
- MASTER_TASKS.md exists but session files are missing
- Task orchestration appears to run but no files are created

## Root Cause
The task_orchestrator.js in versions before 2.7.5 had issues:
1. Incorrect handling of TodoWrite events
2. Files were created in wrong locations
3. Input format mismatch prevented proper execution

## Solution

### Update to Latest Version (v2.7.5+)
```bash
# In your project directory
npx create-claudook@latest
```

### What's Fixed in v2.7.5
- ✅ Proper TodoWrite event handling
- ✅ Files created inside session directories
- ✅ Symlinks to latest files in main tasks directory
- ✅ Parallel execution enabled by default
- ✅ GitHub-compatible task export

### After Updating
New TodoWrite operations will create:
```
.claude/tasks/
├── MASTER_TASKS.md -> session_*/MASTER_TASKS.md
├── EXECUTION_DASHBOARD.md -> session_*/EXECUTION_DASHBOARD.md
└── session_2025-09-15T20-27-12-491Z/
    ├── MASTER_TASKS.md (actual file)
    ├── EXECUTION_DASHBOARD.md (actual file)
    └── GITHUB_TASKS.md (actual file)
```

### Clean Up Old Empty Directories
```bash
# Remove empty session directories
find .claude/tasks -type d -empty -delete
```

## Verification
After updating, test with:
```bash
echo '{"tool":"TodoWrite","params":{"todos":[{"content":"Test task","status":"pending"}]}}' | node .claude/hooks/claudook/task_orchestrator.js
```

You should see:
```
📋 Task Orchestrator: Created N tasks
📁 Tasks saved to: .claude/tasks/session_*/
🚀 Parallel execution groups: N
```