#!/usr/bin/env python3
"""
Claudook - Performance Optimizer
Automatically formats and optimizes code after modifications.
"""
import json
import sys
import os

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


def load_hook_data():
    """Load and parse hook data from stdin."""
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}

def get_optimization_tools(file_extension):
    """Get optimization tools for a specific file extension."""
    
    tools_map = {
        '.py': {
            'formatter': 'black --line-length 88',
            'linter': 'flake8',
            'import_sorter': 'isort',
            'type_checker': 'mypy',
            'description': 'Python optimization'
        },
        '.js': {
            'formatter': 'prettier --write',
            'linter': 'eslint --fix',
            'description': 'JavaScript optimization'
        },
        '.ts': {
            'formatter': 'prettier --write',
            'linter': 'eslint --fix',
            'type_checker': 'tsc --noEmit',
            'description': 'TypeScript optimization'
        },
        '.jsx': {
            'formatter': 'prettier --write',
            'linter': 'eslint --fix',
            'description': 'React JSX optimization'
        },
        '.tsx': {
            'formatter': 'prettier --write',
            'linter': 'eslint --fix',
            'type_checker': 'tsc --noEmit',
            'description': 'React TypeScript optimization'
        },
        '.go': {
            'formatter': 'gofmt -w',
            'linter': 'go vet',
            'imports': 'goimports -w',
            'description': 'Go optimization'
        },
        '.rs': {
            'formatter': 'rustfmt',
            'linter': 'cargo clippy',
            'description': 'Rust optimization'
        },
        '.java': {
            'formatter': 'google-java-format --replace',
            'linter': 'checkstyle',
            'description': 'Java optimization'
        },
        '.cpp': {
            'formatter': 'clang-format -i',
            'linter': 'cppcheck',
            'description': 'C++ optimization'
        },
        '.c': {
            'formatter': 'clang-format -i',
            'linter': 'cppcheck',
            'description': 'C optimization'
        },
        '.cs': {
            'formatter': 'dotnet format',
            'linter': 'dotnet build',
            'description': 'C# optimization'
        },
        '.rb': {
            'formatter': 'rubocop --auto-correct',
            'linter': 'rubocop',
            'description': 'Ruby optimization'
        },
        '.php': {
            'formatter': 'php-cs-fixer fix',
            'linter': 'phpstan analyse',
            'description': 'PHP optimization'
        },
    }
    
    return tools_map.get(file_extension)

def create_optimization_message(file_path, tools):
    """Create optimization message for the file."""
    
    optimization_tasks = [
        f"1. 🎨 Format code: {tools['formatter']}",
        f"2. 🔍 Run linter: {tools.get('linter', 'appropriate linter')}",
    ]
    
    # Add optional tools if available
    if 'import_sorter' in tools:
        optimization_tasks.append(f"3. 📦 Sort imports: {tools['import_sorter']}")
    if 'imports' in tools:
        optimization_tasks.append(f"3. 📦 Optimize imports: {tools['imports']}")
    if 'type_checker' in tools:
        optimization_tasks.append(f"4. 🔍 Type check: {tools['type_checker']}")
    
    # Add final verification steps
    optimization_tasks.extend([
        "5. ✅ Verify syntax and compilation",
        "6. 🧹 Remove unused variables/imports", 
        "7. 📊 Ensure code meets style guidelines"
    ])
    
    return f"""🚀 AUTO-OPTIMIZATION REQUIRED for {file_path}

{tools['description']} workflow:

{chr(10).join(optimization_tasks)}

⚡ Performance Benefits:
• Consistent code style across project
• Early detection of syntax errors  
• Improved code readability
• Reduced technical debt
• Better maintainability

💡 This ensures professional code quality standards.

🚫 You cannot proceed until optimization is complete.
"""

def should_optimize(file_path):
    """Determine if a file should be optimized."""
    
    # Skip if file doesn't exist or is empty
    if not file_path or not os.path.exists(file_path):
        return False
    
    # Skip very large files (> 1MB) to avoid performance issues
    try:
        if os.path.getsize(file_path) > 1024 * 1024:
            return False
    except OSError:
        return False
    
    # Skip files in certain directories
    skip_dirs = [
        'node_modules/', '.git/', '__pycache__/', 
        '.venv/', 'venv/', 'build/', 'dist/',
        '.pytest_cache/', 'target/', '.cargo/'
    ]
    
    if any(skip_dir in file_path for skip_dir in skip_dirs):
        return False
    
    # Skip certain file patterns
    skip_patterns = [
        '.min.js', '.min.css', '.bundle.js', 
        '.generated.', '.auto.', '.lock'
    ]
    
    if any(pattern in file_path for pattern in skip_patterns):
        return False
    
    return True

def main():
    """Main performance optimizer logic."""
    data = load_hook_data()
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    
    # Only process file editing operations
    if tool_name not in ["Edit", "Write"]:
        sys.exit(0)
    
    if not file_path or not should_optimize(file_path):
        sys.exit(0)
    
    # Get file extension
    file_extension = os.path.splitext(file_path)[1].lower()
    
    # Get optimization tools for this file type
    tools = get_optimization_tools(file_extension)
    
    if not tools:
        # No optimization tools for this file type
        sys.exit(0)
    
    # Create and return optimization message
    optimization_message = create_optimization_message(file_path, tools)
    
    output = {
        "decision": "block",
        "reason": optimization_message
    }
    
    print(json.dumps(output))
    sys.exit(2)

if __name__ == "__main__":
    main()
