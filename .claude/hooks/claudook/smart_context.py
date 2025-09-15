#!/usr/bin/env python3
"""
Claudook - Smart Context
Automatically injects relevant project context at session start.
"""
import json
import os
import subprocess
import sys

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


def run_command(cmd):
    """Run a command and return its output, or None if it fails."""
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
        return result.decode().strip()
    except:
        return None

def get_git_context():
    """Get Git repository context."""
    context = []
    
    # Current branch
    branch = run_command('git branch --show-current')
    if branch:
        context.append(f"🌿 Current branch: {branch}")
    
    # Check for uncommitted changes
    status = run_command('git status --porcelain')
    if status:
        changes = len(status.split('\n')) if status else 0
        context.append(f"📝 {changes} uncommitted changes detected")
    
    # Recent commits
    recent_commits = run_command('git log --oneline -3')
    if recent_commits:
        commits = recent_commits.split('\n')
        context.append(f"📚 Recent commits: {len(commits)} (latest: {commits[0][:50]}...)")
    
    return context

def get_node_context():
    """Get Node.js project context."""
    context = []
    
    if os.path.exists('package.json'):
        try:
            with open('package.json') as f:
                pkg = json.load(f)
                name = pkg.get('name', 'Unknown')
                version = pkg.get('version', '?')
                context.append(f"📦 Project: {name} v{version}")
                
                # Scripts
                if 'scripts' in pkg:
                    scripts = list(pkg['scripts'].keys())[:4]  # Show first 4 scripts
                    context.append(f"🔧 Available scripts: {', '.join(scripts)}")
                
                # Dependencies count
                deps = len(pkg.get('dependencies', {}))
                dev_deps = len(pkg.get('devDependencies', {}))
                if deps or dev_deps:
                    context.append(f"📋 Dependencies: {deps} prod, {dev_deps} dev")
                    
        except Exception:
            context.append("📦 Node.js project detected (package.json found)")
    
    # Check for common Node files
    node_files = ['yarn.lock', 'package-lock.json', 'pnpm-lock.yaml', '.nvmrc']
    found_files = [f for f in node_files if os.path.exists(f)]
    if found_files:
        context.append(f"🔒 Lock files: {', '.join(found_files)}")
    
    return context

def get_python_context():
    """Get Python project context."""
    context = []
    
    # Python project files
    python_files = {
        'requirements.txt': 'pip requirements',
        'pyproject.toml': 'modern Python project',
        'setup.py': 'Python package',
        'Pipfile': 'Pipenv project',
        'poetry.lock': 'Poetry project',
        'environment.yml': 'Conda environment'
    }
    
    found = [(f, desc) for f, desc in python_files.items() if os.path.exists(f)]
    if found:
        context.append(f"🐍 Python project: {', '.join([desc for _, desc in found])}")
    
    # Virtual environment
    if os.environ.get('VIRTUAL_ENV'):
        venv_name = os.path.basename(os.environ['VIRTUAL_ENV'])
        context.append(f"🔧 Virtual env active: {venv_name}")
    
    # Python version
    python_version = run_command('python3 --version')
    if python_version:
        context.append(f"🐍 {python_version}")
    
    return context

def get_other_contexts():
    """Get context for other project types."""
    context = []
    
    # Docker
    docker_files = ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml']
    if any(os.path.exists(f) for f in docker_files):
        context.append("🐳 Docker configuration detected")
    
    # Go
    if os.path.exists('go.mod'):
        context.append("🐹 Go module project")
    
    # Rust
    if os.path.exists('Cargo.toml'):
        context.append("🦀 Rust project (Cargo)")
    
    # Java
    java_files = ['pom.xml', 'build.gradle', 'build.gradle.kts']
    if any(os.path.exists(f) for f in java_files):
        context.append("☕ Java project detected")
    
    # .NET
    if any(f.endswith('.csproj') or f.endswith('.sln') for f in os.listdir('.')):
        context.append("🔵 .NET project detected")
    
    # Ruby
    if os.path.exists('Gemfile'):
        context.append("💎 Ruby project (Gemfile)")
    
    # PHP
    if os.path.exists('composer.json'):
        context.append("🐘 PHP project (Composer)")
    
    return context

def get_environment_context():
    """Get current environment context."""
    context = []
    
    # Check for common environment files
    env_files = ['.env', '.env.local', '.env.example', '.env.development']
    found_env = [f for f in env_files if os.path.exists(f)]
    if found_env:
        context.append(f"⚙️ Environment files: {', '.join(found_env)}")
    
    # Check for CI/CD files
    ci_files = ['.github/workflows', '.gitlab-ci.yml', '.circleci', 'Jenkinsfile']
    found_ci = [f for f in ci_files if os.path.exists(f)]
    if found_ci:
        context.append(f"🔄 CI/CD: {', '.join(found_ci)}")
    
    # Error logs
    error_files = ['error.log', 'npm-debug.log', 'yarn-error.log', 'crash.log']
    found_errors = [f for f in error_files if os.path.exists(f) and os.path.getsize(f) > 0]
    if found_errors:
        context.append(f"⚠️ Error logs detected: {', '.join(found_errors)}")
    
    return context

def get_smart_context():
    """Generate comprehensive project context."""
    sections = []

    # Git context
    git_ctx = get_git_context()
    if git_ctx:
        sections.append("📍 Git: " + " • ".join(git_ctx[:2]))  # Branch and changes

    # Project info
    node_ctx = get_node_context()
    if node_ctx:
        # Project name/version and scripts
        project_info = []
        if len(node_ctx) > 0:
            project_info.append(node_ctx[0])  # Name/version
        if len(node_ctx) > 1:
            project_info.append(node_ctx[1])  # Scripts
        if project_info:
            sections.append("📦 " + " • ".join(project_info))

    python_ctx = get_python_context()
    if python_ctx and not node_ctx:
        sections.append("🐍 " + " • ".join(python_ctx[:2]))

    # Other important contexts
    other_ctx = get_other_contexts()
    if other_ctx:
        # Show Docker, CI/CD, etc.
        important_other = [c for c in other_ctx if "🐳" in c or "🔄" in c]
        if important_other:
            sections.append(" • ".join(important_other))

    # Environment warnings (only if critical)
    env_ctx = get_environment_context()
    warnings = [item for item in env_ctx if "⚠️" in item]
    if warnings:
        sections.append(warnings[0])

    if sections:
        return "\n".join(sections)
    else:
        return "📍 Project: " + os.path.basename(os.getcwd())

def main():
    """Main entry point."""
    context = get_smart_context()
    
    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context
        }
    }
    
    print(json.dumps(output))

if __name__ == "__main__":
    main()
