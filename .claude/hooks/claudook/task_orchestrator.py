#!/usr/bin/env python3
"""
Claudook - Task Orchestrator
Intercepts user prompts, decomposes into tasks, and orchestrates parallel execution.
"""
import json
import sys
import os
import re
import hashlib
from datetime import datetime
from pathlib import Path

# Import the agent spawner
sys.path.insert(0, str(Path(__file__).parent))
from agent_spawner import AgentSpawner

# Control file for feature toggle
TASK_DECOMPOSE_ENABLED = os.path.expanduser("~/.claude/parallel_enabled")
TASKS_DIR = Path(".claude/tasks")
CURRENT_SESSION = None

# Task complexity thresholds
COMPLEXITY_KEYWORDS = {
    "simple": ["fix", "update", "change", "modify", "rename", "move"],
    "medium": ["add", "create", "implement", "integrate", "setup"],
    "complex": ["build", "develop", "design", "architect", "refactor", "migrate"]
}

# Task type patterns
TASK_PATTERNS = {
    "api": r"(api|rest|endpoint|route|backend)",
    "frontend": r"(ui|frontend|component|page|form|button)",
    "database": r"(database|db|schema|model|migration)",
    "auth": r"(auth|login|register|jwt|token|password)",
    "test": r"(test|spec|unit|integration|e2e)",
    "docs": r"(document|docs|readme|api.doc|swagger)"
}

# Agent type mapping
AGENT_TYPES = {
    "research": "researcher",
    "analyze": "researcher",
    "investigate": "researcher",
    "design": "architect",
    "plan": "architect",
    "structure": "architect",
    "implement": "coder",
    "code": "coder",
    "develop": "coder",
    "build": "coder",
    "test": "tester",
    "validate": "tester",
    "verify": "tester",
    "document": "documenter",
    "explain": "documenter"
}

class TaskOrchestrator:
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.tasks = []
        self.dependencies = {}
        self.parallel_groups = []
        self.agent_spawner = None

    def analyze_complexity(self, prompt):
        """Analyze the complexity of the user's request."""
        prompt_lower = prompt.lower()

        # Check for complex keywords
        for level, keywords in COMPLEXITY_KEYWORDS.items():
            if any(keyword in prompt_lower for keyword in keywords):
                if level == "complex":
                    return 3
                elif level == "medium":
                    return 2
        return 1

    def detect_task_type(self, prompt):
        """Detect the type of task from the prompt."""
        prompt_lower = prompt.lower()
        detected_types = []

        for task_type, pattern in TASK_PATTERNS.items():
            if re.search(pattern, prompt_lower):
                detected_types.append(task_type)

        return detected_types if detected_types else ["general"]

    def decompose_tasks(self, prompt, complexity, task_types):
        """Decompose the request into subtasks based on complexity and type."""
        tasks = []
        task_id = 1

        # Research phase (always first for complex tasks)
        if complexity >= 2:
            tasks.append({
                "id": f"{task_id:03d}",
                "name": "research",
                "description": f"Research best practices and existing solutions",
                "agent_type": "researcher",
                "dependencies": [],
                "estimated_time": "5 min",
                "parallel_safe": True
            })
            task_id += 1

        # Design phase for complex tasks
        if complexity >= 3:
            tasks.append({
                "id": f"{task_id:03d}",
                "name": "design",
                "description": f"Design system architecture and structure",
                "agent_type": "architect",
                "dependencies": [],
                "estimated_time": "10 min",
                "parallel_safe": True
            })
            task_id += 1

        # Task-specific implementation
        for task_type in task_types:
            if task_type == "api":
                tasks.extend(self._create_api_tasks(task_id))
                task_id += 3
            elif task_type == "auth":
                tasks.extend(self._create_auth_tasks(task_id))
                task_id += 4
            elif task_type == "frontend":
                tasks.extend(self._create_frontend_tasks(task_id))
                task_id += 2
            elif task_type == "database":
                tasks.extend(self._create_database_tasks(task_id))
                task_id += 2

        # Testing phase (always after implementation)
        if complexity >= 2:
            test_deps = [t["id"] for t in tasks if "implement" in t["name"] or "create" in t["name"]]
            tasks.append({
                "id": f"{task_id:03d}",
                "name": "test",
                "description": "Create and run comprehensive tests",
                "agent_type": "tester",
                "dependencies": test_deps[-2:] if len(test_deps) >= 2 else test_deps,
                "estimated_time": "10 min",
                "parallel_safe": False
            })
            task_id += 1

        # Documentation (can run in parallel)
        tasks.append({
            "id": f"{task_id:03d}",
            "name": "document",
            "description": "Create comprehensive documentation",
            "agent_type": "documenter",
            "dependencies": [],
            "estimated_time": "5 min",
            "parallel_safe": True
        })

        return tasks

    def _create_api_tasks(self, start_id):
        """Create API-specific tasks."""
        return [
            {
                "id": f"{start_id:03d}",
                "name": "design_api",
                "description": "Design API endpoints and structure",
                "agent_type": "architect",
                "dependencies": ["001"] if start_id > 1 else [],
                "estimated_time": "5 min",
                "parallel_safe": True
            },
            {
                "id": f"{start_id+1:03d}",
                "name": "implement_api",
                "description": "Implement API endpoints",
                "agent_type": "coder",
                "dependencies": [f"{start_id:03d}"],
                "estimated_time": "15 min",
                "parallel_safe": False
            },
            {
                "id": f"{start_id+2:03d}",
                "name": "api_validation",
                "description": "Add input validation and error handling",
                "agent_type": "coder",
                "dependencies": [f"{start_id+1:03d}"],
                "estimated_time": "5 min",
                "parallel_safe": False
            }
        ]

    def _create_auth_tasks(self, start_id):
        """Create authentication-specific tasks."""
        return [
            {
                "id": f"{start_id:03d}",
                "name": "user_model",
                "description": "Create user model and database schema",
                "agent_type": "coder",
                "dependencies": ["002"] if start_id > 2 else [],
                "estimated_time": "5 min",
                "parallel_safe": False
            },
            {
                "id": f"{start_id+1:03d}",
                "name": "registration",
                "description": "Implement user registration",
                "agent_type": "coder",
                "dependencies": [f"{start_id:03d}"],
                "estimated_time": "10 min",
                "parallel_safe": False
            },
            {
                "id": f"{start_id+2:03d}",
                "name": "login",
                "description": "Implement login with JWT",
                "agent_type": "coder",
                "dependencies": [f"{start_id:03d}"],
                "estimated_time": "10 min",
                "parallel_safe": False
            },
            {
                "id": f"{start_id+3:03d}",
                "name": "auth_middleware",
                "description": "Create authentication middleware",
                "agent_type": "coder",
                "dependencies": [f"{start_id+2:03d}"],
                "estimated_time": "5 min",
                "parallel_safe": False
            }
        ]

    def _create_frontend_tasks(self, start_id):
        """Create frontend-specific tasks."""
        return [
            {
                "id": f"{start_id:03d}",
                "name": "ui_components",
                "description": "Create UI components",
                "agent_type": "coder",
                "dependencies": ["002"] if start_id > 2 else [],
                "estimated_time": "10 min",
                "parallel_safe": True
            },
            {
                "id": f"{start_id+1:03d}",
                "name": "ui_integration",
                "description": "Integrate components with backend",
                "agent_type": "coder",
                "dependencies": [f"{start_id:03d}"],
                "estimated_time": "10 min",
                "parallel_safe": False
            }
        ]

    def _create_database_tasks(self, start_id):
        """Create database-specific tasks."""
        return [
            {
                "id": f"{start_id:03d}",
                "name": "schema_design",
                "description": "Design database schema",
                "agent_type": "architect",
                "dependencies": ["001"] if start_id > 1 else [],
                "estimated_time": "5 min",
                "parallel_safe": True
            },
            {
                "id": f"{start_id+1:03d}",
                "name": "migration",
                "description": "Create database migrations",
                "agent_type": "coder",
                "dependencies": [f"{start_id:03d}"],
                "estimated_time": "5 min",
                "parallel_safe": False
            }
        ]

    def identify_parallel_groups(self, tasks):
        """Identify which tasks can run in parallel."""
        groups = []
        processed = set()

        # Build dependency map
        dep_map = {task["id"]: task["dependencies"] for task in tasks}

        # Find tasks with no dependencies (can run immediately)
        level_0 = [task for task in tasks if not task["dependencies"]]
        if level_0:
            groups.append(level_0)
            processed.update(task["id"] for task in level_0)

        # Find subsequent levels
        while len(processed) < len(tasks):
            next_level = []
            for task in tasks:
                if task["id"] not in processed:
                    # Check if all dependencies are processed
                    if all(dep in processed for dep in task["dependencies"]):
                        next_level.append(task)

            if next_level:
                # Check if tasks can actually run in parallel (no file conflicts)
                parallel_safe = [t for t in next_level if t.get("parallel_safe", True)]
                sequential = [t for t in next_level if not t.get("parallel_safe", True)]

                if parallel_safe:
                    groups.append(parallel_safe)
                for task in sequential:
                    groups.append([task])

                processed.update(task["id"] for task in next_level)
            else:
                break

        return groups

    def create_individual_task_files(self, tasks, session_dir):
        """Create individual task files for each decomposed task."""
        tasks_dir = session_dir / "tasks"

        for task in tasks:
            task_file = tasks_dir / f"task_{task['id']}.md"

            content = f"""# Task {task['id']}: {task['name']}

## Description
{task['description']}

## Details
- **Agent Type**: {task['agent_type']}
- **Estimated Time**: {task['estimated_time']}
- **Parallel Safe**: {'Yes' if task.get('parallel_safe', True) else 'No'}

## Dependencies
{', '.join(task['dependencies']) if task['dependencies'] else 'None'}

## Status
- **Current State**: Pending
- **Started**: Not yet
- **Completed**: Not yet

## Execution Plan
1. Initialize {task['agent_type']} agent
2. Load task context
3. Execute task
4. Validate results
5. Report completion

## Output
*To be generated during execution*

## Logs
*Execution logs will appear here*
"""

            with open(task_file, "w") as f:
                f.write(content)

    def create_agent_configs(self, tasks, session_dir):
        """Create agent configurations for all tasks."""
        # Initialize agent spawner
        self.agent_spawner = AgentSpawner(self.session_id)

        # Update agent directories to use session folder
        agents_dir = session_dir / "agents"
        outputs_dir = session_dir / "outputs"

        # Spawn agents for all tasks
        for task in tasks:
            agent = self.agent_spawner.spawn_agent(task)

            # Save agent configuration to session folder
            agent_config_file = agents_dir / f"agent_{agent.id}_{agent.type}.json"
            config_data = {
                "id": agent.id,
                "type": agent.type,
                "task": task,
                "session_id": self.session_id,
                "created_at": agent.created_at.isoformat(),
                "status": agent.status,
                "role": agent.config["role"],
                "tools": agent.config["tools"],
                "prompt": agent.generate_prompt()
            }

            with open(agent_config_file, "w") as f:
                json.dump(config_data, f, indent=2)

        # Generate agent summary
        agent_summary_file = agents_dir / "AGENT_SUMMARY.md"
        summary_content = f"""# Agent Configuration Summary
## Session: {self.session_id}

### Total Agents: {len(tasks)}

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
"""
        for agent_id, agent in self.agent_spawner.agents.items():
            summary_content += f"| {agent.id} | {agent.type} | {agent.task.get('name', 'unknown')} | {agent.status} |\n"

        with open(agent_summary_file, "w") as f:
            f.write(summary_content)

    def create_master_tasks_file(self, prompt, tasks, parallel_groups):
        """Create the MASTER_TASKS.md file."""
        session_dir = TASKS_DIR / f"session_{self.session_id}"
        session_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        (session_dir / "tasks").mkdir(exist_ok=True)
        (session_dir / "agents").mkdir(exist_ok=True)
        (session_dir / "outputs").mkdir(exist_ok=True)

        # Write to session folder instead of main directory
        master_file = session_dir / "MASTER_TASKS.md"

        content = f"""# 📋 Master Task List
## Session: {self.session_id}
### Request: "{prompt}"

## Overview
- **Total Tasks**: {len(tasks)}
- **Parallel Groups**: {len(parallel_groups)}
- **Estimated Time**: {sum(int(t['estimated_time'].split()[0]) for t in tasks)} minutes
- **Complexity**: {self.analyze_complexity(prompt)} / 3

## Execution Plan

"""

        # Add parallel groups
        for i, group in enumerate(parallel_groups, 1):
            content += f"### Phase {i}: "
            if len(group) > 1:
                content += f"Parallel Execution ({len(group)} agents)\n"
                content += "```\n"
                for task in group:
                    content += f"[{task['agent_type']}] {task['description']}\n"
                content += "```\n"
            else:
                task = group[0]
                content += f"Sequential - {task['agent_type']}\n"
                content += f"- {task['description']}\n"
            content += "\n"

        # Add detailed task list
        content += "## Detailed Tasks\n\n"
        for task in tasks:
            deps = f" (depends on: {', '.join(task['dependencies'])})" if task['dependencies'] else ""
            content += f"- [ ] **{task['id']}** - {task['description']}{deps}\n"
            content += f"  - Agent: {task['agent_type']}\n"
            content += f"  - Time: {task['estimated_time']}\n"
            content += f"  - Parallel Safe: {'Yes' if task.get('parallel_safe', True) else 'No'}\n\n"

        # Add progress tracking
        content += """## Progress Tracking

- [ ] Phase 1: Research & Analysis
- [ ] Phase 2: Design & Architecture
- [ ] Phase 3: Implementation
- [ ] Phase 4: Testing & Validation
- [ ] Phase 5: Documentation

### Status: ⏳ Ready to Execute
"""

        with open(master_file, "w") as f:
            f.write(content)

        # Create individual task files
        self.create_individual_task_files(tasks, session_dir)

        # Create agent configurations
        self.create_agent_configs(tasks, session_dir)

        return master_file

    def create_execution_dashboard(self, tasks, parallel_groups):
        """Create live execution dashboard."""
        session_dir = TASKS_DIR / f"session_{self.session_id}"
        dashboard_file = session_dir / "EXECUTION_DASHBOARD.md"

        content = f"""# 🎯 Parallel Execution Dashboard
## Session: {self.session_id}
### Status: 🟢 Active

## Current Phase: 1 / {len(parallel_groups)}

### Active Agents
| Agent | Task | Status | Progress | ETA |
|-------|------|--------|----------|-----|
"""

        # Add placeholder for active agents
        if parallel_groups and len(parallel_groups[0]) > 0:
            for task in parallel_groups[0][:3]:  # Show first 3 tasks
                content += f"| {task['agent_type']} | {task['description'][:30]}... | 🔄 Starting | ░░░░░░░░░░ 0% | {task['estimated_time']} |\n"

        content += """

### Completed Tasks
None yet

### Queued Tasks
"""

        queued_count = len(tasks) - (len(parallel_groups[0]) if parallel_groups else 0)
        content += f"{queued_count} tasks waiting\n"

        content += """

### Resource Usage
- **Active Agents**: 0 / 5
- **Memory Usage**: 0%
- **Parallel Efficiency**: 0%

### Execution Timeline
```
[00:00] System initialized
[00:00] Task decomposition complete
[00:00] Ready to execute
```

---
*Dashboard updates automatically during execution*
"""

        with open(dashboard_file, "w") as f:
            f.write(content)

        return dashboard_file

    def generate_context_injection(self, tasks, parallel_groups, master_file):
        """Generate context to inject into Claude's response."""

        # Create TodoWrite items
        todo_items = []
        for task in tasks:
            todo_items.append({
                "content": f"[{task['id']}] {task['description']}",
                "status": "pending",
                "activeForm": f"Working on {task['name']}"
            })

        context = f"""
🧠 TASK ORCHESTRATION COMPLETE

I've analyzed your request and created an intelligent execution plan with {len(tasks)} tasks organized into {len(parallel_groups)} execution phases.

📊 Execution Strategy:
"""

        # Describe parallel execution plan
        for i, group in enumerate(parallel_groups, 1):
            if len(group) > 1:
                agents = ", ".join([t['agent_type'] for t in group])
                context += f"• Phase {i}: PARALLEL execution with {len(group)} agents ({agents})\n"
            else:
                context += f"• Phase {i}: Sequential - {group[0]['agent_type']} agent\n"

        context += f"""

📁 Task Files Created:
• Session Folder: .claude/tasks/session_{self.session_id}/
  ├── MASTER_TASKS.md - Overall task plan
  ├── EXECUTION_DASHBOARD.md - Live status tracking
  ├── tasks/ - {len(tasks)} individual task files
  ├── agents/ - Agent configurations (to be populated)
  └── outputs/ - Task outputs (to be generated)

🚀 Ready to Execute:
The system will now proceed with Phase 1. Multiple specialized agents will work in parallel where possible.

💡 Commands Available:
• /task-status - View current progress
• /agent-status - See active agents
• /task-complete [id] - Mark task complete

Starting execution now...
"""

        # Add TodoWrite synchronization instruction
        context += "\n\n[System: Populating TodoWrite with task list...]"

        return context, todo_items

def main():
    """Main entry point for the task orchestrator hook."""

    # Check if feature is enabled
    if not os.path.exists(TASK_DECOMPOSE_ENABLED):
        # Feature disabled, pass through
        sys.exit(0)

    try:
        # Read input from stdin
        data = json.load(sys.stdin)
        prompt = data.get("prompt", "")

        if not prompt:
            sys.exit(0)

        # Initialize orchestrator
        orchestrator = TaskOrchestrator()

        # Analyze request
        complexity = orchestrator.analyze_complexity(prompt)
        task_types = orchestrator.detect_task_type(prompt)

        # Only decompose if complexity is medium or higher
        if complexity < 2:
            sys.exit(0)

        # Decompose into tasks
        tasks = orchestrator.decompose_tasks(prompt, complexity, task_types)

        # Identify parallel groups
        parallel_groups = orchestrator.identify_parallel_groups(tasks)

        # Create task files
        master_file = orchestrator.create_master_tasks_file(prompt, tasks, parallel_groups)
        dashboard_file = orchestrator.create_execution_dashboard(tasks, parallel_groups)

        # Also create symlinks in main directory for backwards compatibility
        main_master = TASKS_DIR / "MASTER_TASKS.md"
        main_dashboard = TASKS_DIR / "EXECUTION_DASHBOARD.md"

        # Remove old files if they exist
        if main_master.exists():
            main_master.unlink()
        if main_dashboard.exists():
            main_dashboard.unlink()

        # Create symlinks to session files
        main_master.symlink_to(master_file.relative_to(TASKS_DIR))
        main_dashboard.symlink_to(dashboard_file.relative_to(TASKS_DIR))

        # Generate context injection
        context, todo_items = orchestrator.generate_context_injection(tasks, parallel_groups, master_file)

        # Output hook response
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context,
                "metadata": {
                    "task_count": len(tasks),
                    "parallel_groups": len(parallel_groups),
                    "session_id": orchestrator.session_id,
                    "todo_items": todo_items
                }
            }
        }

        print(json.dumps(output))

    except Exception as e:
        # Log error but don't break Claude
        if os.environ.get("CLAUDOOK_DEBUG"):
            print(f"Task orchestrator error: {e}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()