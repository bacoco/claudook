#!/usr/bin/env python3
"""
Claudook - Smart Context
Automatically injects relevant project context at session start.
"""
import json
import os
import subprocess

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
    all_context = []
    
    # Git context
    git_ctx = get_git_context()
    all_context.extend(git_ctx)
    
    # Project type contexts
    node_ctx = get_node_context()
    all_context.extend(node_ctx)
    
    python_ctx = get_python_context()
    all_context.extend(python_ctx)
    
    other_ctx = get_other_contexts()
    all_context.extend(other_ctx)
    
    # Environment context
    env_ctx = get_environment_context()
    all_context.extend(env_ctx)
    
    if all_context:
        return "AUTO PROJECT CONTEXT:\n" + "\n".join(all_context)
    else:
        return "AUTO PROJECT CONTEXT:\n📁 Basic project directory"

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
