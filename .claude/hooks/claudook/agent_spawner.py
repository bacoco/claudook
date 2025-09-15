#!/usr/bin/env python3
"""
Claudook - Agent Spawner
Creates and manages specialized agents for parallel task execution.
"""
import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

# Agent configuration directory
AGENT_CONFIG_DIR = Path(".claude/tasks/agent_configs")
AGENT_OUTPUT_DIR = Path(".claude/tasks/outputs")

class AgentType:
    """Defines different agent types and their specializations."""

    RESEARCHER = {
        "name": "researcher",
        "role": "Research Specialist",
        "prompt": """You are a research specialist focused on gathering information and analyzing requirements.
Your primary responsibilities:
- Research best practices and industry standards
- Analyze existing code and documentation
- Investigate technical solutions and alternatives
- Provide comprehensive analysis reports
- Identify potential challenges and risks

Focus only on research and analysis. Do not implement code.""",
        "tools": ["WebSearch", "Read", "Grep", "WebFetch"],
        "capabilities": ["analysis", "investigation", "documentation_review"],
        "output_format": "markdown_report"
    }

    ARCHITECT = {
        "name": "architect",
        "role": "System Architect",
        "prompt": """You are a system architect focused on design and structure.
Your primary responsibilities:
- Design system architecture and component structure
- Create database schemas and data models
- Define API specifications and interfaces
- Plan system integration points
- Document architectural decisions

Focus on design and planning. Create specifications but do not implement.""",
        "tools": ["Read", "Write", "Grep"],
        "capabilities": ["system_design", "schema_creation", "api_design"],
        "output_format": "technical_specification"
    }

    CODER = {
        "name": "coder",
        "role": "Implementation Specialist",
        "prompt": """You are an implementation specialist focused on writing high-quality code.
Your primary responsibilities:
- Implement features according to specifications
- Write clean, maintainable code
- Follow best practices and coding standards
- Optimize for performance and scalability
- Add appropriate error handling

Focus on implementation. Follow the provided specifications exactly.""",
        "tools": ["Write", "Edit", "MultiEdit", "Read", "Bash"],
        "capabilities": ["coding", "implementation", "optimization"],
        "output_format": "code_files"
    }

    TESTER = {
        "name": "tester",
        "role": "Quality Assurance Specialist",
        "prompt": """You are a QA specialist focused on testing and validation.
Your primary responsibilities:
- Create comprehensive test suites
- Write unit and integration tests
- Perform validation and verification
- Identify bugs and edge cases
- Ensure code coverage

Focus on testing. Create and run tests to validate the implementation.""",
        "tools": ["Read", "Write", "Bash", "Grep"],
        "capabilities": ["testing", "validation", "quality_assurance"],
        "output_format": "test_report"
    }

    DOCUMENTER = {
        "name": "documenter",
        "role": "Documentation Specialist",
        "prompt": """You are a documentation specialist focused on creating clear documentation.
Your primary responsibilities:
- Write comprehensive documentation
- Create API documentation
- Document code with comments
- Write user guides and tutorials
- Create README files

Focus on documentation. Make complex topics easy to understand.""",
        "tools": ["Read", "Write", "Edit"],
        "capabilities": ["documentation", "technical_writing", "tutorials"],
        "output_format": "documentation"
    }

    REVIEWER = {
        "name": "reviewer",
        "role": "Code Review Specialist",
        "prompt": """You are a code review specialist focused on quality and standards.
Your primary responsibilities:
- Review code for quality and standards
- Identify potential bugs and issues
- Suggest improvements and optimizations
- Check for security vulnerabilities
- Ensure best practices are followed

Focus on review and feedback. Provide constructive criticism.""",
        "tools": ["Read", "Grep", "Bash"],
        "capabilities": ["code_review", "security_audit", "optimization_suggestions"],
        "output_format": "review_report"
    }

    @classmethod
    def get_agent_type(cls, name: str) -> Dict:
        """Get agent configuration by name."""
        agents = {
            "researcher": cls.RESEARCHER,
            "architect": cls.ARCHITECT,
            "coder": cls.CODER,
            "tester": cls.TESTER,
            "documenter": cls.DOCUMENTER,
            "reviewer": cls.REVIEWER
        }
        return agents.get(name, cls.CODER)  # Default to coder


class Agent:
    """Represents a specialized agent instance."""

    def __init__(self, agent_type: str, task: Dict, session_id: str = None):
        self.id = str(uuid.uuid4())[:8]
        self.type = agent_type
        self.config = AgentType.get_agent_type(agent_type)
        self.task = task
        self.session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.created_at = datetime.now()
        self.status = "created"
        self.output_file = None

    def generate_prompt(self) -> str:
        """Generate the specific prompt for this agent's task."""
        base_prompt = self.config["prompt"]

        task_prompt = f"""
# Task Assignment
**Task ID**: {self.task.get('id', 'unknown')}
**Description**: {self.task.get('description', '')}
**Estimated Time**: {self.task.get('estimated_time', '10 min')}

## Dependencies
"""

        deps = self.task.get('dependencies', [])
        if deps:
            task_prompt += f"This task depends on: {', '.join(deps)}\n"
            task_prompt += "Review the outputs from these tasks before proceeding.\n"
        else:
            task_prompt += "No dependencies - you can start immediately.\n"

        task_prompt += f"""
## Deliverables
Please provide your output in {self.config['output_format']} format.
Save your results to: {self.get_output_path()}

## Available Tools
You have access to: {', '.join(self.config['tools'])}

## Instructions
1. Focus only on your specialized role
2. Complete the task as described
3. Provide clear, well-documented output
4. Save results to the specified location

Begin working on the task now.
"""

        return base_prompt + "\n\n" + task_prompt

    def get_output_path(self) -> Path:
        """Get the output file path for this agent."""
        if not self.output_file:
            filename = f"task_{self.task.get('id', 'unknown')}_{self.type}_{self.id}.md"
            self.output_file = AGENT_OUTPUT_DIR / self.session_id / filename
        return self.output_file

    def get_config_path(self) -> Path:
        """Get the configuration file path for this agent."""
        filename = f"agent_{self.id}_{self.type}.json"
        return AGENT_CONFIG_DIR / self.session_id / filename

    def save_config(self):
        """Save agent configuration to file."""
        config_path = self.get_config_path()
        config_path.parent.mkdir(parents=True, exist_ok=True)

        config_data = {
            "id": self.id,
            "type": self.type,
            "task": self.task,
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "output_file": str(self.output_file) if self.output_file else None,
            "config": self.config,
            "prompt": self.generate_prompt()
        }

        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=2)

    def to_dict(self) -> Dict:
        """Convert agent to dictionary."""
        return {
            "id": self.id,
            "type": self.type,
            "role": self.config["role"],
            "task_id": self.task.get("id"),
            "task_description": self.task.get("description"),
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "output_file": str(self.output_file) if self.output_file else None
        }


class AgentSpawner:
    """Manages creation and lifecycle of specialized agents."""

    def __init__(self, session_id: str = None, max_parallel_agents: int = 5):
        self.session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.max_parallel_agents = max_parallel_agents
        self.agents = {}
        self.active_agents = []
        self.completed_agents = []
        self.agent_queue = []

    def determine_agent_type(self, task: Dict) -> str:
        """Determine the best agent type for a task."""
        task_name = task.get("name", "").lower()
        description = task.get("description", "").lower()
        agent_type = task.get("agent_type", "")

        if agent_type:
            return agent_type

        # Pattern matching for agent type
        if any(word in task_name or word in description
               for word in ["research", "analyze", "investigate", "explore"]):
            return "researcher"
        elif any(word in task_name or word in description
                 for word in ["design", "architect", "plan", "schema", "structure"]):
            return "architect"
        elif any(word in task_name or word in description
                 for word in ["test", "validate", "verify", "check"]):
            return "tester"
        elif any(word in task_name or word in description
                 for word in ["document", "docs", "readme", "explain"]):
            return "documenter"
        elif any(word in task_name or word in description
                 for word in ["review", "audit", "check", "analyze"]):
            return "reviewer"
        else:
            return "coder"  # Default to coder

    def spawn_agent(self, task: Dict) -> Agent:
        """Spawn a new agent for a task."""
        agent_type = self.determine_agent_type(task)
        agent = Agent(agent_type, task, self.session_id)

        # Save configuration
        agent.save_config()

        # Track agent
        self.agents[agent.id] = agent

        # Check if we can activate immediately
        if len(self.active_agents) < self.max_parallel_agents:
            self.activate_agent(agent)
        else:
            self.agent_queue.append(agent)

        return agent

    def spawn_parallel_group(self, tasks: List[Dict]) -> List[Agent]:
        """Spawn multiple agents for parallel execution."""
        agents = []

        for task in tasks:
            agent = self.spawn_agent(task)
            agents.append(agent)

        return agents

    def activate_agent(self, agent: Agent):
        """Activate an agent for execution."""
        agent.status = "active"
        self.active_agents.append(agent)

    def complete_agent(self, agent_id: str, output: Optional[str] = None):
        """Mark an agent as completed."""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            agent.status = "completed"

            # Remove from active list
            self.active_agents = [a for a in self.active_agents if a.id != agent_id]
            self.completed_agents.append(agent)

            # Save output if provided
            if output:
                output_path = agent.get_output_path()
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "w") as f:
                    f.write(output)

            # Activate next queued agent if any
            if self.agent_queue and len(self.active_agents) < self.max_parallel_agents:
                next_agent = self.agent_queue.pop(0)
                self.activate_agent(next_agent)

    def get_status(self) -> Dict:
        """Get current status of all agents."""
        return {
            "session_id": self.session_id,
            "total_agents": len(self.agents),
            "active_agents": len(self.active_agents),
            "completed_agents": len(self.completed_agents),
            "queued_agents": len(self.agent_queue),
            "max_parallel": self.max_parallel_agents,
            "agents": {
                "active": [a.to_dict() for a in self.active_agents],
                "completed": [a.to_dict() for a in self.completed_agents],
                "queued": [a.to_dict() for a in self.agent_queue]
            }
        }

    def generate_agent_report(self) -> str:
        """Generate a report of all agents and their status."""
        report = f"""# Agent Execution Report
## Session: {self.session_id}

### Summary
- Total Agents: {len(self.agents)}
- Active: {len(self.active_agents)}
- Completed: {len(self.completed_agents)}
- Queued: {len(self.agent_queue)}

### Active Agents
"""

        for agent in self.active_agents:
            report += f"- **{agent.id}** ({agent.type}): {agent.task.get('description', 'No description')}\n"

        report += "\n### Completed Agents\n"
        for agent in self.completed_agents:
            report += f"- ✅ **{agent.id}** ({agent.type}): {agent.task.get('description', 'No description')}\n"
            if agent.output_file:
                report += f"  - Output: {agent.output_file}\n"

        report += "\n### Queued Agents\n"
        for agent in self.agent_queue:
            report += f"- ⏳ **{agent.id}** ({agent.type}): {agent.task.get('description', 'No description')}\n"

        return report

    def generate_task_instructions(self, parallel_groups: List[List[Dict]]) -> str:
        """Generate instructions for executing tasks with agents."""
        instructions = """# Task Execution Instructions

## Using the Task Tool

I'll now execute these tasks using specialized agents. Here's the execution plan:

"""

        for i, group in enumerate(parallel_groups, 1):
            instructions += f"### Phase {i}\n"

            if len(group) > 1:
                instructions += "Running in PARALLEL:\n```python\n"
                for task in group:
                    agent_type = self.determine_agent_type(task)
                    instructions += f'Task("{agent_type}", "{task.get("description", "")}")\n'
                instructions += "```\n\n"
            else:
                task = group[0]
                agent_type = self.determine_agent_type(task)
                instructions += f"Running SEQUENTIAL:\n"
                instructions += f'```python\nTask("{agent_type}", "{task.get("description", "")}")\n```\n\n'

        return instructions


def create_agents_for_tasks(tasks: List[Dict], parallel_groups: List[List[str]],
                            session_id: str = None) -> AgentSpawner:
    """Create agents for task execution."""
    spawner = AgentSpawner(session_id)

    # Create task map
    task_map = {task["id"]: task for task in tasks}

    # Spawn agents for each group
    for group in parallel_groups:
        group_tasks = [task_map[task_id] for task_id in group if task_id in task_map]
        spawner.spawn_parallel_group(group_tasks)

    return spawner


if __name__ == "__main__":
    # Test the agent spawner
    test_tasks = [
        {"id": "001", "description": "Research authentication methods", "name": "research"},
        {"id": "002", "description": "Design API structure", "name": "design"},
        {"id": "003", "description": "Implement user model", "name": "implement"}
    ]

    spawner = AgentSpawner()
    for task in test_tasks:
        agent = spawner.spawn_agent(task)
        print(f"Spawned {agent.type} agent {agent.id} for task {task['id']}")

    print("\nStatus:")
    print(json.dumps(spawner.get_status(), indent=2))