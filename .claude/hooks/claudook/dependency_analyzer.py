#!/usr/bin/env python3
"""
Claudook - Dependency Analyzer
Builds Directed Acyclic Graphs (DAG) for task dependencies and identifies parallel execution opportunities.
"""
import json
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict, deque

from pathlib import Path

# Robust path resolution - find and change to project root
def find_project_root():
    """Find project root by looking for .claude directory"""
    current = Path.cwd().resolve()

    # Search up the directory tree
    for path in [current] + list(current.parents):
        if (path / ".claude").is_dir():
            return path

    # Fallback: check if we're already in .claude/hooks/claudook
    if current.name == "claudook" and current.parent.name == "hooks":
        return current.parent.parent.parent

    return None

# Apply the fix before any other operations
project_root = find_project_root()
if project_root:
    os.chdir(project_root)
else:
    # If can't find project root, exit gracefully
    sys.exit(0)


class DependencyGraph:
    """Represents a task dependency graph with parallel execution analysis."""

    def __init__(self):
        self.nodes = {}  # task_id -> task_data
        self.edges = defaultdict(set)  # task_id -> set of dependencies
        self.reverse_edges = defaultdict(set)  # task_id -> set of dependents
        self.levels = {}  # task_id -> execution level
        self.parallel_groups = []

    def add_task(self, task_id: str, task_data: Dict):
        """Add a task node to the graph."""
        self.nodes[task_id] = task_data

    def add_dependency(self, task_id: str, depends_on: str):
        """Add a dependency edge."""
        self.edges[task_id].add(depends_on)
        self.reverse_edges[depends_on].add(task_id)

    def detect_cycles(self) -> bool:
        """Detect if there are any cycles in the dependency graph."""
        visited = set()
        rec_stack = set()

        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.edges.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node in self.nodes:
            if node not in visited:
                if has_cycle(node):
                    return True
        return False

    def topological_sort(self) -> List[str]:
        """Perform topological sort to get valid execution order."""
        in_degree = {node: len(self.edges.get(node, [])) for node in self.nodes}
        queue = deque([node for node in self.nodes if in_degree[node] == 0])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)

            for neighbor in self.reverse_edges.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(result) != len(self.nodes):
            raise ValueError("Cycle detected in dependency graph")

        return result

    def calculate_levels(self):
        """Calculate execution levels for parallel grouping."""
        self.levels = {}
        visited = set()

        def get_level(node):
            if node in self.levels:
                return self.levels[node]

            if not self.edges[node]:  # No dependencies
                self.levels[node] = 0
                return 0

            # Level is 1 + max level of dependencies
            max_dep_level = max(get_level(dep) for dep in self.edges[node])
            self.levels[node] = max_dep_level + 1
            return self.levels[node]

        for node in self.nodes:
            get_level(node)

    def identify_parallel_groups(self) -> List[List[str]]:
        """Identify groups of tasks that can run in parallel."""
        self.calculate_levels()

        # Group tasks by level
        level_groups = defaultdict(list)
        for task_id, level in self.levels.items():
            level_groups[level].append(task_id)

        # Sort levels and create groups
        self.parallel_groups = []
        for level in sorted(level_groups.keys()):
            tasks = level_groups[level]

            # Check for file conflicts within the group
            safe_parallel = []
            unsafe_tasks = []

            for task_id in tasks:
                task = self.nodes[task_id]
                if task.get("parallel_safe", True):
                    safe_parallel.append(task_id)
                else:
                    unsafe_tasks.append(task_id)

            # Add safe parallel tasks as one group
            if safe_parallel:
                self.parallel_groups.append(safe_parallel)

            # Add unsafe tasks as individual groups
            for task_id in unsafe_tasks:
                self.parallel_groups.append([task_id])

        return self.parallel_groups

    def get_critical_path(self) -> Tuple[List[str], int]:
        """Find the critical path (longest path) through the graph."""
        # Calculate earliest start times
        earliest_start = {}
        sorted_nodes = self.topological_sort()

        for node in sorted_nodes:
            if not self.edges[node]:  # No dependencies
                earliest_start[node] = 0
            else:
                max_end_time = 0
                for dep in self.edges[node]:
                    dep_task = self.nodes[dep]
                    dep_time = int(dep_task.get("estimated_time", "5").split()[0])
                    max_end_time = max(max_end_time, earliest_start[dep] + dep_time)
                earliest_start[node] = max_end_time

        # Find the path
        critical_path = []
        max_time = 0

        # Reconstruct path
        def find_path(node, current_path, current_time):
            nonlocal critical_path, max_time
            task_time = int(self.nodes[node].get("estimated_time", "5").split()[0])
            new_time = current_time + task_time
            new_path = current_path + [node]

            if not self.reverse_edges[node]:  # No dependents
                if new_time > max_time:
                    max_time = new_time
                    critical_path = new_path
            else:
                for dependent in self.reverse_edges[node]:
                    find_path(dependent, new_path, new_time)

        # Start from nodes with no dependencies
        for node in sorted_nodes:
            if not self.edges[node]:
                find_path(node, [], 0)

        return critical_path, max_time

    def can_parallelize(self, task1: str, task2: str) -> bool:
        """Check if two tasks can run in parallel."""
        # Tasks can parallelize if neither depends on the other
        if task2 in self.get_all_dependencies(task1):
            return False
        if task1 in self.get_all_dependencies(task2):
            return False

        # Check if both are marked as parallel safe
        t1_safe = self.nodes[task1].get("parallel_safe", True)
        t2_safe = self.nodes[task2].get("parallel_safe", True)

        return t1_safe and t2_safe

    def get_all_dependencies(self, task_id: str) -> Set[str]:
        """Get all transitive dependencies of a task."""
        visited = set()

        def visit(node):
            if node in visited:
                return
            visited.add(node)
            for dep in self.edges.get(node, []):
                visit(dep)

        visit(task_id)
        visited.discard(task_id)  # Remove self
        return visited

    def get_all_dependents(self, task_id: str) -> Set[str]:
        """Get all tasks that depend on this task."""
        visited = set()

        def visit(node):
            if node in visited:
                return
            visited.add(node)
            for dep in self.reverse_edges.get(node, []):
                visit(dep)

        visit(task_id)
        visited.discard(task_id)  # Remove self
        return visited

    def visualize_graph(self) -> str:
        """Generate ASCII visualization of the dependency graph."""
        lines = ["# Dependency Graph Visualization\n"]

        # Group by levels
        self.calculate_levels()
        level_groups = defaultdict(list)
        for task_id, level in self.levels.items():
            level_groups[level].append(task_id)

        # Draw each level
        for level in sorted(level_groups.keys()):
            lines.append(f"\n## Level {level}")
            tasks = level_groups[level]

            for task_id in tasks:
                task = self.nodes[task_id]
                deps = list(self.edges.get(task_id, []))
                dep_str = f" <- {', '.join(deps)}" if deps else " (no deps)"
                lines.append(f"- [{task_id}] {task.get('description', '')}

{dep_str}")

        # Add parallel groups
        lines.append("\n## Parallel Execution Groups")
        for i, group in enumerate(self.parallel_groups, 1):
            if len(group) > 1:
                lines.append(f"\n### Group {i} (Parallel)")
                for task_id in group:
                    task = self.nodes[task_id]
                    lines.append(f"- [{task_id}] {task.get('description', '')}")
            else:
                lines.append(f"\n### Group {i} (Sequential)")
                task_id = group[0]
                task = self.nodes[task_id]
                lines.append(f"- [{task_id}] {task.get('description', '')}")

        return "\n".join(lines)

    def get_execution_plan(self) -> Dict:
        """Generate complete execution plan."""
        critical_path, critical_time = self.get_critical_path()

        plan = {
            "total_tasks": len(self.nodes),
            "parallel_groups": len(self.parallel_groups),
            "critical_path": critical_path,
            "minimum_time": critical_time,
            "execution_order": self.topological_sort(),
            "parallel_efficiency": self.calculate_parallel_efficiency(),
            "groups": []
        }

        # Add detailed group information
        for i, group in enumerate(self.parallel_groups, 1):
            group_info = {
                "phase": i,
                "parallel": len(group) > 1,
                "tasks": []
            }

            for task_id in group:
                task = self.nodes[task_id]
                group_info["tasks"].append({
                    "id": task_id,
                    "description": task.get("description", ""),
                    "agent_type": task.get("agent_type", "generic"),
                    "estimated_time": task.get("estimated_time", "5 min"),
                    "dependencies": list(self.edges.get(task_id, []))
                })

            plan["groups"].append(group_info)

        return plan

    def calculate_parallel_efficiency(self) -> float:
        """Calculate how efficiently tasks are parallelized."""
        if not self.parallel_groups:
            return 0.0

        # Count tasks that are in parallel groups
        parallel_tasks = sum(
            len(group) for group in self.parallel_groups if len(group) > 1
        )

        total_tasks = len(self.nodes)
        if total_tasks == 0:
            return 0.0

        return (parallel_tasks / total_tasks) * 100


class DependencyAnalyzer:
    """Main analyzer for task dependencies."""

    def __init__(self):
        self.graph = DependencyGraph()

    def analyze_tasks(self, tasks: List[Dict]) -> Dict:
        """Analyze task list and build dependency graph."""
        # Build graph
        for task in tasks:
            self.graph.add_task(task["id"], task)

            # Add dependencies
            for dep in task.get("dependencies", []):
                self.graph.add_dependency(task["id"], dep)

        # Check for cycles
        if self.graph.detect_cycles():
            raise ValueError("Circular dependencies detected in task list")

        # Identify parallel groups
        self.graph.identify_parallel_groups()

        # Generate execution plan
        execution_plan = self.graph.get_execution_plan()

        # Add visualization
        execution_plan["visualization"] = self.graph.visualize_graph()

        return execution_plan

    def optimize_dependencies(self, tasks: List[Dict]) -> List[Dict]:
        """Optimize task dependencies for maximum parallelization."""
        optimized = []

        for task in tasks:
            task_copy = task.copy()

            # Remove redundant dependencies
            deps = set(task.get("dependencies", []))
            necessary_deps = deps.copy()

            # Remove transitive dependencies
            for dep in deps:
                # Get all dependencies of this dependency
                trans_deps = self.graph.get_all_dependencies(dep)
                # Remove any that are also direct dependencies
                necessary_deps -= trans_deps

            task_copy["dependencies"] = list(necessary_deps)
            optimized.append(task_copy)

        return optimized

    def suggest_parallelization(self, tasks: List[Dict]) -> List[Dict]:
        """Suggest modifications to improve parallelization."""
        suggestions = []

        # Analyze current parallel efficiency
        current_efficiency = self.graph.calculate_parallel_efficiency()

        if current_efficiency < 50:
            suggestions.append({
                "type": "efficiency",
                "message": f"Low parallel efficiency ({current_efficiency:.1f}%)",
                "suggestion": "Consider breaking down large tasks or removing unnecessary dependencies"
            })

        # Check for long sequential chains
        critical_path, critical_time = self.graph.get_critical_path()
        if len(critical_path) > 5:
            suggestions.append({
                "type": "critical_path",
                "message": f"Long critical path with {len(critical_path)} sequential tasks",
                "suggestion": "Consider if some tasks can be made independent",
                "path": critical_path
            })

        # Check for bottleneck tasks
        for task_id, dependents in self.graph.reverse_edges.items():
            if len(dependents) > 3:
                suggestions.append({
                    "type": "bottleneck",
                    "message": f"Task {task_id} is blocking {len(dependents)} other tasks",
                    "suggestion": "Consider splitting this task or starting it earlier",
                    "blocked_tasks": list(dependents)
                })

        return suggestions


def analyze_dependencies(tasks: List[Dict]) -> Dict:
    """Main entry point for dependency analysis."""
    analyzer = DependencyAnalyzer()
    return analyzer.analyze_tasks(tasks)


if __name__ == "__main__":
    # Test the dependency analyzer
    test_tasks = [
        {"id": "001", "description": "Research", "dependencies": [], "parallel_safe": True},
        {"id": "002", "description": "Design", "dependencies": [], "parallel_safe": True},
        {"id": "003", "description": "Implement Backend", "dependencies": ["001", "002"], "parallel_safe": False},
        {"id": "004", "description": "Implement Frontend", "dependencies": ["002"], "parallel_safe": False},
        {"id": "005", "description": "Testing", "dependencies": ["003", "004"], "parallel_safe": True},
        {"id": "006", "description": "Documentation", "dependencies": [], "parallel_safe": True}
    ]

    result = analyze_dependencies(test_tasks)
    print(json.dumps(result, indent=2))