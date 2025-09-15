#!/usr/bin/env python3
"""
Claudook - Git Backup System
Suggests creating backup branches for significant changes.
"""
import json
import sys
import os
import subprocess
from datetime import datetime

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

def run_git_command(command):
    """Run a git command and return output, or None if it fails."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return None

def is_git_repository():
    """Check if current directory is a git repository."""
    return run_git_command('git rev-parse --git-dir') is not None

def get_git_status():
    """Get number of uncommitted changes."""
    status = run_git_command('git status --porcelain')
    if status:
        return len([line for line in status.split('\n') if line.strip()])
    return 0

def get_current_branch():
    """Get current git branch name."""
    branch = run_git_command('git branch --show-current')
    return branch if branch else 'main'

def is_critical_file(file_path):
    """Determine if a file is critical for the project."""
    if not file_path:
        return False
    
    # Configuration and build files
    critical_files = [
        'package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
        'requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile', 'poetry.lock',
        'Cargo.toml', 'Cargo.lock', 
        'pom.xml', 'build.gradle', 'build.gradle.kts',
        'go.mod', 'go.sum',
        'Dockerfile', 'docker-compose.yml', 'docker-compose.yaml',
        '.env.example', 'env.template',
        'tsconfig.json', 'jsconfig.json',
        'webpack.config.js', 'vite.config.js', 'rollup.config.js',
        'babel.config.js', '.babelrc',
        'jest.config.js', '.jestrc',
        'eslint.config.js', '.eslintrc.js', '.eslintrc.json',
        'prettier.config.js', '.prettierrc',
        'README.md', 'CHANGELOG.md', 'LICENSE',
        'Makefile', 'CMakeLists.txt',
        '.github/workflows', '.gitlab-ci.yml', '.circleci/config.yml',
        'vercel.json', 'netlify.toml'
    ]
    
    # Check if file name matches critical files
    file_name = os.path.basename(file_path)
    if file_name in critical_files:
        return True
    
    # Check if path contains critical directories
    critical_dirs = [
        '.github/workflows/', '.gitlab-ci/', '.circleci/',
        'migrations/', 'alembic/', 'database/',
        'schemas/', 'models/',
        'config/', 'configs/'
    ]
    
    for critical_dir in critical_dirs:
        if critical_dir in file_path:
            return True
    
    return False

def is_large_change(content):
    """Determine if the content represents a large change."""
    if not content:
        return False
    
    # Consider large if more than 500 lines
    if len(content.split('\n')) > 500:
        return True
    
    # Consider large if more than 10KB
    if len(content) > 10 * 1024:
        return True
    
    return False

def has_many_changes():
    """Check if there are many uncommitted changes."""
    return get_git_status() > 5

def should_suggest_backup(file_path, content):
    """Determine if backup should be suggested."""
    return (
        is_critical_file(file_path) or
        is_large_change(content) or
        has_many_changes()
    )

def create_backup_suggestion(file_path, content):
    """Create backup suggestion message."""
    
    # Generate branch name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = os.path.basename(file_path).replace('.', '_') if file_path else "changes"
    branch_name = f"claude-backup-{safe_filename}-{timestamp}"
    current_branch = get_current_branch()
    
    # Determine change significance
    reasons = []
    if is_critical_file(file_path):
        reasons.append("📋 Critical project file")
    if is_large_change(content):
        reasons.append("📊 Large code change")
    if has_many_changes():
        reasons.append("🔄 Multiple uncommitted files")
    
    reason_text = " • ".join(reasons) if reasons else "Significant modification detected"
    
    return f"""💾 BACKUP RECOMMENDED for {file_path}

🎯 Change Significance:
{reason_text}

🌿 GIT BACKUP SUGGESTION:

1. 📸 CREATE backup branch:
   git checkout -b {branch_name}

2. 💾 COMMIT current state:
   git add .
   git commit -m "Backup before Claude modifications: {os.path.basename(file_path)}"

3. 🔄 RETURN to working branch:
   git checkout {current_branch}

4. ✅ PROCEED with changes safely

🛡️ Safety Benefits:
• Complete rollback capability
• Change history preservation  
• Safe experimentation environment
• Team collaboration safety

📋 Recovery Commands (if needed later):
   git checkout {branch_name}          # Switch to backup
   git cherry-pick <commit-hash>       # Apply specific changes
   git merge {branch_name}            # Merge backup changes

💡 Alternative: If you're confident, proceed without backup.

⚠️ This is a suggestion, not a requirement.
"""

def main():
    """Main git backup logic."""
    # Only run if we're in a git repository
    if not is_git_repository():
        sys.exit(0)
    
    data = load_hook_data()
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    content = tool_input.get("content", "")
    
    # Only process file modification operations
    if tool_name not in ["Edit", "Write"]:
        sys.exit(0)
    
    # Check if backup should be suggested
    if not should_suggest_backup(file_path, content):
        sys.exit(0)
    
    # Create and display backup suggestion (but don't block)
    backup_message = create_backup_suggestion(file_path, content)
    
    # Print to stderr so it shows as a warning, not blocking
    print(backup_message, file=sys.stderr)
    
    # Don't block the operation, just suggest
    sys.exit(0)

if __name__ == "__main__":
    main()
