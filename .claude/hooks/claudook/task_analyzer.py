#!/usr/bin/env python3
"""
Claudook - Task Analyzer
Advanced task analysis and pattern recognition for intelligent decomposition.
"""
import re
import json
from typing import List, Dict, Tuple, Optional

class TaskAnalyzer:
    """Analyzes user prompts to understand task requirements and complexity."""

    def __init__(self):
        # Expanded complexity scoring
        self.complexity_scores = {
            # Simple operations (score: 1)
            "fix": 1, "update": 1, "change": 1, "modify": 1, "rename": 1,
            "move": 1, "delete": 1, "remove": 1, "correct": 1, "adjust": 1,

            # Medium operations (score: 2-3)
            "add": 2, "create": 2, "implement": 3, "integrate": 3, "setup": 2,
            "install": 2, "configure": 2, "extend": 2, "enhance": 2, "improve": 2,

            # Complex operations (score: 4-5)
            "build": 4, "develop": 4, "design": 4, "architect": 5, "refactor": 4,
            "migrate": 5, "restructure": 5, "optimize": 4, "scale": 5, "deploy": 4
        }

        # Action verb patterns for task detection
        self.action_patterns = {
            "research": ["research", "analyze", "investigate", "explore", "study", "review"],
            "design": ["design", "architect", "plan", "structure", "model", "schema"],
            "implement": ["implement", "code", "develop", "build", "create", "write"],
            "test": ["test", "validate", "verify", "check", "ensure", "confirm"],
            "document": ["document", "explain", "describe", "annotate", "comment"],
            "optimize": ["optimize", "improve", "enhance", "speed up", "refactor"],
            "debug": ["debug", "fix", "solve", "troubleshoot", "resolve"],
            "deploy": ["deploy", "release", "publish", "launch", "ship"]
        }

        # Component patterns for feature detection
        self.component_patterns = {
            "authentication": ["auth", "login", "signup", "register", "jwt", "token", "session", "oauth"],
            "api": ["api", "rest", "graphql", "endpoint", "route", "controller", "webhook"],
            "database": ["database", "db", "table", "schema", "migration", "query", "sql", "nosql"],
            "frontend": ["ui", "frontend", "component", "page", "form", "button", "modal", "layout"],
            "backend": ["backend", "server", "service", "middleware", "handler", "processor"],
            "testing": ["test", "spec", "unit", "integration", "e2e", "coverage", "mock"],
            "security": ["security", "encryption", "ssl", "https", "sanitize", "validate", "protect"],
            "performance": ["performance", "cache", "optimize", "speed", "latency", "throughput"]
        }

        # Technology stack patterns
        self.tech_patterns = {
            "javascript": ["javascript", "js", "node", "npm", "typescript", "ts"],
            "python": ["python", "py", "pip", "django", "flask", "fastapi"],
            "react": ["react", "jsx", "hooks", "component", "redux", "next"],
            "vue": ["vue", "vuex", "nuxt", "composition"],
            "database": ["postgres", "mysql", "mongodb", "redis", "sqlite"],
            "cloud": ["aws", "gcp", "azure", "docker", "kubernetes", "serverless"]
        }

        # Time estimation factors (in minutes)
        self.time_estimates = {
            "research": 5,
            "design": 10,
            "implement_simple": 10,
            "implement_medium": 20,
            "implement_complex": 30,
            "test_unit": 5,
            "test_integration": 10,
            "document": 5,
            "review": 5
        }

    def analyze_prompt(self, prompt: str) -> Dict:
        """Comprehensive analysis of the user prompt."""
        prompt_lower = prompt.lower()

        analysis = {
            "original_prompt": prompt,
            "complexity_score": self.calculate_complexity(prompt_lower),
            "detected_actions": self.detect_actions(prompt_lower),
            "detected_components": self.detect_components(prompt_lower),
            "detected_technologies": self.detect_technologies(prompt_lower),
            "estimated_time": self.estimate_total_time(prompt_lower),
            "requires_research": self.needs_research(prompt_lower),
            "requires_testing": self.needs_testing(prompt_lower),
            "parallelizable": self.check_parallelizable(prompt_lower),
            "task_count_estimate": self.estimate_task_count(prompt_lower)
        }

        return analysis

    def calculate_complexity(self, prompt: str) -> int:
        """Calculate complexity score based on keywords."""
        score = 0
        word_count = len(prompt.split())

        # Base complexity from keywords
        for word, value in self.complexity_scores.items():
            if word in prompt:
                score += value

        # Additional complexity factors
        if "and" in prompt:
            score += prompt.count("and")  # Multiple requirements
        if "with" in prompt:
            score += 1  # Additional features
        if "integrate" in prompt or "integration" in prompt:
            score += 2  # Integration complexity
        if "migrate" in prompt or "refactor" in prompt:
            score += 3  # High complexity operations

        # Word count factor
        if word_count > 20:
            score += 2
        if word_count > 40:
            score += 3

        return min(score, 10)  # Cap at 10

    def detect_actions(self, prompt: str) -> List[str]:
        """Detect action verbs in the prompt."""
        detected = []
        for action_type, patterns in self.action_patterns.items():
            if any(pattern in prompt for pattern in patterns):
                detected.append(action_type)
        return detected if detected else ["implement"]  # Default to implement

    def detect_components(self, prompt: str) -> List[str]:
        """Detect system components mentioned in the prompt."""
        detected = []
        for component, patterns in self.component_patterns.items():
            if any(pattern in prompt for pattern in patterns):
                detected.append(component)
        return detected

    def detect_technologies(self, prompt: str) -> List[str]:
        """Detect technologies mentioned in the prompt."""
        detected = []
        for tech, patterns in self.tech_patterns.items():
            if any(pattern in prompt for pattern in patterns):
                detected.append(tech)
        return detected

    def estimate_total_time(self, prompt: str) -> int:
        """Estimate total time in minutes."""
        base_time = 10
        complexity = self.calculate_complexity(prompt)

        # Add time based on complexity
        time = base_time + (complexity * 5)

        # Add time for specific components
        components = self.detect_components(prompt)
        time += len(components) * 5

        # Add time for testing if needed
        if self.needs_testing(prompt):
            time += 10

        return time

    def needs_research(self, prompt: str) -> bool:
        """Determine if research phase is needed."""
        research_indicators = [
            "best practice", "how to", "compare", "vs", "versus",
            "recommend", "suggestion", "option", "alternative",
            "investigate", "explore", "analyze"
        ]
        return any(indicator in prompt for indicator in research_indicators)

    def needs_testing(self, prompt: str) -> bool:
        """Determine if testing is required."""
        # Almost always need testing except for simple changes
        if self.calculate_complexity(prompt) >= 2:
            return True
        return "test" in prompt or "validate" in prompt

    def check_parallelizable(self, prompt: str) -> bool:
        """Check if tasks can be parallelized."""
        # Multiple components often mean parallelizable
        components = self.detect_components(prompt)
        return len(components) > 1

    def estimate_task_count(self, prompt: str) -> int:
        """Estimate number of subtasks."""
        base_count = 3  # Minimum: implement, test, document

        complexity = self.calculate_complexity(prompt)
        components = self.detect_components(prompt)
        actions = self.detect_actions(prompt)

        # Add tasks based on complexity
        count = base_count + (complexity // 2)

        # Add tasks for each component
        count += len(components)

        # Add tasks for each action type
        count += len(actions)

        return count

    def generate_task_template(self, analysis: Dict) -> List[Dict]:
        """Generate task template based on analysis."""
        tasks = []
        task_id = 1

        # Research phase if needed
        if analysis["requires_research"]:
            tasks.append({
                "id": task_id,
                "type": "research",
                "name": "Research and Analysis",
                "description": "Research best practices and analyze requirements",
                "estimated_time": self.time_estimates["research"],
                "dependencies": [],
                "agent_type": "researcher"
            })
            task_id += 1

        # Design phase for complex tasks
        if analysis["complexity_score"] >= 4:
            tasks.append({
                "id": task_id,
                "type": "design",
                "name": "System Design",
                "description": "Design architecture and create specifications",
                "estimated_time": self.time_estimates["design"],
                "dependencies": [1] if analysis["requires_research"] else [],
                "agent_type": "architect"
            })
            task_id += 1

        # Implementation tasks
        for component in analysis["detected_components"]:
            tasks.append({
                "id": task_id,
                "type": "implement",
                "name": f"Implement {component}",
                "description": f"Develop {component} functionality",
                "estimated_time": self.time_estimates["implement_medium"],
                "dependencies": list(range(1, task_id)),
                "agent_type": "coder"
            })
            task_id += 1

        # Testing if required
        if analysis["requires_testing"]:
            impl_tasks = [t["id"] for t in tasks if t["type"] == "implement"]
            tasks.append({
                "id": task_id,
                "type": "test",
                "name": "Testing and Validation",
                "description": "Create and run comprehensive tests",
                "estimated_time": self.time_estimates["test_integration"],
                "dependencies": impl_tasks,
                "agent_type": "tester"
            })
            task_id += 1

        # Documentation
        tasks.append({
            "id": task_id,
            "type": "document",
            "name": "Documentation",
            "description": "Create comprehensive documentation",
            "estimated_time": self.time_estimates["document"],
            "dependencies": [],  # Can run in parallel
            "agent_type": "documenter"
        })

        return tasks

    def identify_dependencies(self, tasks: List[Dict]) -> Dict[int, List[int]]:
        """Identify task dependencies based on logical flow."""
        dependencies = {}

        for task in tasks:
            task_id = task["id"]
            deps = []

            # Research must come first
            if task["type"] != "research":
                research_tasks = [t["id"] for t in tasks if t["type"] == "research"]
                if research_tasks and task["type"] in ["design", "implement"]:
                    deps.extend(research_tasks)

            # Design must come before implementation
            if task["type"] == "implement":
                design_tasks = [t["id"] for t in tasks if t["type"] == "design"]
                deps.extend(design_tasks)

            # Testing depends on implementation
            if task["type"] == "test":
                impl_tasks = [t["id"] for t in tasks if t["type"] == "implement"]
                deps.extend(impl_tasks)

            # Documentation can usually run in parallel
            if task["type"] == "document":
                deps = []  # No dependencies

            dependencies[task_id] = deps

        return dependencies

    def optimize_parallel_execution(self, tasks: List[Dict]) -> List[List[Dict]]:
        """Optimize task grouping for parallel execution."""
        groups = []
        completed = set()
        dependencies = self.identify_dependencies(tasks)

        while len(completed) < len(tasks):
            # Find tasks that can run now
            available = []
            for task in tasks:
                if task["id"] not in completed:
                    task_deps = dependencies.get(task["id"], [])
                    if all(dep in completed for dep in task_deps):
                        available.append(task)

            if not available:
                break

            # Group by parallelizable tasks
            parallel_group = []
            sequential_group = []

            for task in available:
                # Documentation and research can run in parallel
                if task["type"] in ["research", "document", "design"]:
                    parallel_group.append(task)
                else:
                    sequential_group.append(task)

            # Add parallel group if exists
            if parallel_group:
                groups.append(parallel_group)
                completed.update(t["id"] for t in parallel_group)

            # Add sequential tasks one by one
            for task in sequential_group:
                groups.append([task])
                completed.add(task["id"])

        return groups


def analyze_request(prompt: str) -> Dict:
    """Main entry point for task analysis."""
    analyzer = TaskAnalyzer()
    analysis = analyzer.analyze_prompt(prompt)

    # Generate task template
    tasks = analyzer.generate_task_template(analysis)

    # Optimize for parallel execution
    parallel_groups = analyzer.optimize_parallel_execution(tasks)

    analysis["generated_tasks"] = tasks
    analysis["parallel_groups"] = parallel_groups

    return analysis


if __name__ == "__main__":
    # Test the analyzer
    test_prompt = "Build a complete REST API with user authentication, including registration, login, JWT tokens, and comprehensive tests"

    result = analyze_request(test_prompt)
    print(json.dumps(result, indent=2))