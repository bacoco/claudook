#!/usr/bin/env python3
"""
Claudook - Analytics Tracker
Tracks coding patterns and productivity metrics.
"""
import json
import sys
import os
from datetime import datetime, date

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

def ensure_analytics_directory():
    """Ensure analytics directory exists."""
    analytics_dir = os.path.expanduser("~/.claude/analytics")
    os.makedirs(analytics_dir, exist_ok=True)
    return analytics_dir

def create_analytics_event(data):
    """Create analytics event from hook data."""
    
    # Extract file information
    file_path = data.get("tool_input", {}).get("file_path", "")
    file_extension = ""
    file_size = 0
    
    if file_path:
        file_extension = os.path.splitext(file_path)[1].lower()
        try:
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
        except OSError:
            pass
    
    # Extract command information
    command = data.get("tool_input", {}).get("command", "")
    if command:
        command = command[:200]  # Truncate very long commands
    
    # Create comprehensive event
    event = {
        # Basic info
        "timestamp": datetime.now().isoformat(),
        "date": date.today().isoformat(),
        "hour": datetime.now().hour,
        "weekday": datetime.now().weekday(),  # 0=Monday, 6=Sunday
        
        # Session info
        "session_id": data.get("session_id", "unknown")[:16],  # Truncate for privacy
        "hook_event": data.get("hook_event_name", "unknown"),
        
        # Tool info
        "tool_name": data.get("tool_name", ""),
        "tool_category": categorize_tool(data.get("tool_name", "")),
        
        # File info
        "file_path": file_path,
        "file_extension": file_extension,
        "file_size": file_size,
        "file_language": get_language_from_extension(file_extension),
        
        # Command info (for Bash tools)
        "command": command,
        "command_category": categorize_command(command),
        
        # Project context
        "project_type": detect_project_type(),
        "git_repo": is_git_repository(),
    }
    
    return event

def categorize_tool(tool_name):
    """Categorize tool by type."""
    categories = {
        "file_ops": ["Edit", "Write", "Read", "MultiEdit"],
        "system": ["Bash"],
        "search": ["Glob", "Grep"],
        "web": ["WebFetch", "WebSearch"],
        "task": ["Task"],
        "notebook": ["Notebook"]
    }
    
    for category, tools in categories.items():
        if tool_name in tools:
            return category
    
    return "other"

def categorize_command(command):
    """Categorize bash command by type."""
    if not command:
        return "none"
    
    command_lower = command.lower()
    
    categories = {
        "package_mgmt": ["npm", "pip", "yarn", "pnpm", "cargo", "go get", "composer"],
        "version_control": ["git", "svn", "hg"],
        "build": ["make", "cmake", "gradle", "mvn", "cargo build", "go build"],
        "test": ["pytest", "jest", "npm test", "go test", "cargo test"],
        "file_ops": ["cp", "mv", "rm", "mkdir", "touch", "chmod"],
        "process": ["ps", "kill", "nohup", "screen", "tmux"],
        "network": ["curl", "wget", "ping", "ssh", "scp"],
        "system": ["ls", "cd", "pwd", "find", "grep", "awk", "sed"]
    }
    
    for category, commands in categories.items():
        if any(cmd in command_lower for cmd in commands):
            return category
    
    return "other"

def get_language_from_extension(extension):
    """Get programming language from file extension."""
    language_map = {
        ".py": "Python",
        ".js": "JavaScript", 
        ".ts": "TypeScript",
        ".jsx": "React",
        ".tsx": "React TypeScript",
        ".go": "Go",
        ".rs": "Rust",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".cs": "C#",
        ".rb": "Ruby",
        ".php": "PHP",
        ".sh": "Shell",
        ".sql": "SQL",
        ".html": "HTML",
        ".css": "CSS",
        ".scss": "SCSS",
        ".md": "Markdown",
        ".json": "JSON",
        ".yaml": "YAML",
        ".yml": "YAML",
        ".xml": "XML"
    }
    
    return language_map.get(extension, "Unknown")

def detect_project_type():
    """Detect current project type based on files present."""
    project_indicators = {
        "Node.js": ["package.json"],
        "Python": ["requirements.txt", "pyproject.toml", "setup.py"],
        "Go": ["go.mod"],
        "Rust": ["Cargo.toml"],
        "Java": ["pom.xml", "build.gradle"],
        "PHP": ["composer.json"],
        "Ruby": ["Gemfile"],
        ".NET": ["*.csproj", "*.sln"],
        "Docker": ["Dockerfile"],
    }
    
    for project_type, indicators in project_indicators.items():
        for indicator in indicators:
            if os.path.exists(indicator) or any(f.endswith(indicator.replace("*", "")) for f in os.listdir(".")):
                return project_type
    
    return "Unknown"

def is_git_repository():
    """Check if current directory is a git repository."""
    return os.path.exists(".git") or os.path.exists("../.git")

def log_event(event):
    """Log event to analytics files."""
    analytics_dir = ensure_analytics_directory()
    
    # Log to detailed events file
    events_file = os.path.join(analytics_dir, "events.jsonl")
    with open(events_file, "a") as f:
        f.write(json.dumps(event) + "\n")

def update_daily_stats(event):
    """Update daily statistics."""
    analytics_dir = ensure_analytics_directory()
    daily_file = os.path.join(analytics_dir, f"daily_{event['date']}.json")
    
    # Load existing stats or create new
    if os.path.exists(daily_file):
        with open(daily_file, "r") as f:
            stats = json.load(f)
    else:
        stats = {
            "date": event["date"],
            "total_commands": 0,
            "files_modified": 0,
            "unique_sessions": [],
            "languages": {},
            "tools": {},
            "commands": {},
            "project_types": {},
            "hourly_activity": [0] * 24,
            "first_activity": None,
            "last_activity": None
        }
    
    # Update stats
    stats["total_commands"] += 1
    
    if event["file_path"]:
        stats["files_modified"] += 1
    
    # Track unique sessions
    if event["session_id"] not in stats["unique_sessions"]:
        stats["unique_sessions"].append(event["session_id"])
    
    # Track languages
    if event["file_language"] and event["file_language"] != "Unknown":
        stats["languages"][event["file_language"]] = stats["languages"].get(event["file_language"], 0) + 1
    
    # Track tools
    if event["tool_name"]:
        stats["tools"][event["tool_name"]] = stats["tools"].get(event["tool_name"], 0) + 1
    
    # Track command categories
    if event["command_category"] and event["command_category"] != "none":
        stats["commands"][event["command_category"]] = stats["commands"].get(event["command_category"], 0) + 1
    
    # Track project types
    if event["project_type"] and event["project_type"] != "Unknown":
        stats["project_types"][event["project_type"]] = stats["project_types"].get(event["project_type"], 0) + 1
    
    # Track hourly activity
    stats["hourly_activity"][event["hour"]] += 1
    
    # Track first and last activity
    if not stats["first_activity"]:
        stats["first_activity"] = event["timestamp"]
    stats["last_activity"] = event["timestamp"]
    
    # Save updated stats
    with open(daily_file, "w") as f:
        json.dump(stats, f, indent=2)

def cleanup_old_files():
    """Clean up old analytics files (keep last 30 days)."""
    analytics_dir = ensure_analytics_directory()
    
    try:
        from datetime import timedelta
        cutoff_date = date.today() - timedelta(days=30)
        
        for filename in os.listdir(analytics_dir):
            if filename.startswith("daily_") and filename.endswith(".json"):
                file_date_str = filename.replace("daily_", "").replace(".json", "")
                try:
                    file_date = datetime.strptime(file_date_str, "%Y-%m-%d").date()
                    if file_date < cutoff_date:
                        os.remove(os.path.join(analytics_dir, filename))
                except ValueError:
                    pass  # Skip malformed filenames
    except Exception:
        pass  # Fail silently if cleanup fails

def main():
    """Main analytics tracker logic."""
    data = load_hook_data()
    
    # Skip if no meaningful data
    if not data.get("tool_name"):
        sys.exit(0)
    
    try:
        # Create analytics event
        event = create_analytics_event(data)
        
        # Log event
        log_event(event)
        
        # Update daily stats
        update_daily_stats(event)
        
        # Occasional cleanup (1% chance)
        import random
        if random.random() < 0.01:
            cleanup_old_files()
            
    except Exception:
        # Fail silently to avoid disrupting hooks
        pass
    
    sys.exit(0)

if __name__ == "__main__":
    main()
