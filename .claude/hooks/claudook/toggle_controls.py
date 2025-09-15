#!/usr/bin/env python3
"""
Claudook - Toggle Controls
Easy on/off controls for Claudook features.
"""
import os
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


# Control file paths
CHOICES_FILE = os.path.expanduser("~/.claude/choices_enabled")
TESTS_FILE = os.path.expanduser("~/.claude/tests_enabled")
PARALLEL_FILE = os.path.expanduser("~/.claude/parallel_enabled")

def enable_choices():
    """Enable the multiple choices system."""
    try:
        with open(CHOICES_FILE, 'w') as f:
            f.write("enabled\n")
        print("✅ Multiple choices system ENABLED")
        print("   Claude will now offer A/B/C options for complex questions")
    except IOError as e:
        print(f"❌ Failed to enable choices: {e}")

def disable_choices():
    """Disable the multiple choices system."""
    try:
        if os.path.exists(CHOICES_FILE):
            os.remove(CHOICES_FILE)
        print("❌ Multiple choices system DISABLED")
        print("   Claude will respond directly without offering options")
    except IOError as e:
        print(f"❌ Failed to disable choices: {e}")

def enable_tests():
    """Enable the automatic testing system."""
    try:
        with open(TESTS_FILE, 'w') as f:
            f.write("enabled\n")
        print("✅ Automatic testing ENABLED")
        print("   Claude will be forced to create and run tests after code changes")
    except IOError as e:
        print(f"❌ Failed to enable tests: {e}")

def disable_tests():
    """Disable the automatic testing system."""
    try:
        if os.path.exists(TESTS_FILE):
            os.remove(TESTS_FILE)
        print("❌ Automatic testing DISABLED")
        print("   Claude will not be forced to create tests")
    except IOError as e:
        print(f"❌ Failed to disable tests: {e}")

def enable_parallel():
    """Enable the parallel task execution system."""
    try:
        with open(PARALLEL_FILE, 'w') as f:
            f.write("enabled\n")
        print("✅ Parallel task execution ENABLED")
        print("   Claude will decompose complex tasks and execute them in parallel")
    except IOError as e:
        print(f"❌ Failed to enable parallel execution: {e}")

def disable_parallel():
    """Disable the parallel task execution system."""
    try:
        if os.path.exists(PARALLEL_FILE):
            os.remove(PARALLEL_FILE)
        print("❌ Parallel task execution DISABLED")
        print("   Claude will execute tasks sequentially")
    except IOError as e:
        print(f"❌ Failed to disable parallel execution: {e}")

def show_status():
    """Show current status of all features."""
    choices_status = "🟢 ON" if os.path.exists(CHOICES_FILE) else "🔴 OFF"
    tests_status = "🟢 ON" if os.path.exists(TESTS_FILE) else "🔴 OFF"
    parallel_status = "🟢 ON" if os.path.exists(PARALLEL_FILE) else "🔴 OFF"
    
    print(f"""
🚀 CLAUDOOK STATUS
=====================

📊 Feature Status:
  🎯 Multiple Choice System: {choices_status}
  🧪 Automatic Testing:      {tests_status}
  🚀 Parallel Task Execution: {parallel_status}

💡 Claudook Commands:
  /claudook/help            - Show all available commands
  /claudook/status          - Show this status
  /claudook/choices-enable  - Turn on A/B/C option system
  /claudook/choices-disable - Turn off A/B/C option system
  /claudook/tests-enable    - Turn on mandatory testing
  /claudook/tests-disable   - Turn off mandatory testing
  /claudook/parallel-enable - Turn on parallel task execution
  /claudook/parallel-disable - Turn off parallel task execution

🎨 More Commands:
  /claudook/security-check  - Run security analysis
  /claudook/performance-check - Analyze performance
  /claudook/lint            - Code quality checks
  /claudook/config-show     - View configuration
  /claudook/update          - Check for updates

🎛️ Quick Toggle:
  python3 ~/.claude/hooks/claudook/toggle_controls.py enable-choices
  python3 ~/.claude/hooks/claudook/toggle_controls.py enable-tests
  python3 ~/.claude/hooks/claudook/toggle_controls.py enable-parallel
  python3 ~/.claude/hooks/claudook/toggle_controls.py disable-choices
  python3 ~/.claude/hooks/claudook/toggle_controls.py disable-tests
  python3 ~/.claude/hooks/claudook/toggle_controls.py disable-parallel

📚 Features Overview:

🎯 Multiple Choice System:
   When enabled, Claude automatically offers A/B/C options for complex 
   questions, helping you choose the best approach before implementation.

🧪 Automatic Testing:
   When enabled, Claude is blocked after code changes until it creates
   comprehensive tests and ensures they pass. No exceptions.

🚀 Parallel Task Execution:
   When enabled, Claude automatically decomposes complex requests into
   subtasks, analyzes dependencies, and executes independent tasks in
   parallel using specialized agents.

🔍 Other Active Features:
   ✅ Security Guard (always active)
   ✅ Performance Optimizer (always active) 
   ✅ Documentation Enforcer (always active)
   ✅ Git Backup Suggestions (always active)
   ✅ Usage Analytics (always active)

🎉 Your Claude CLI is enhanced with Claudook!
    """.strip())

def show_help():
    """Show help information."""
    print("""
Claudook Toggle Controls
===========================

USAGE:
  toggle_controls.py [COMMAND]

COMMANDS:
  enable-choices    Enable A/B/C option system
  disable-choices   Disable A/B/C option system
  enable-tests      Enable mandatory testing
  disable-tests     Disable mandatory testing
  status            Show current status (default)
  help              Show this help

EXAMPLES:
  python3 ~/.claude/hooks/claudook/toggle_controls.py enable-choices
  python3 ~/.claude/hooks/claudook/toggle_controls.py status

IN CLAUDE CLI:
  Use slash commands for easier control:
  /claudook/help
  /claudook/status
  /claudook/choices-enable
  /claudook/tests-enable
  /claudook/parallel-enable

FEATURES:
  🎯 Multiple Choices - Get A/B/C options for complex questions
  🧪 Automatic Tests  - Mandatory test creation and execution
""")

def main():
    """Main entry point for toggle controls."""
    
    # Create .claude directory if it doesn't exist
    claude_dir = os.path.expanduser("~/.claude")
    os.makedirs(claude_dir, exist_ok=True)
    
    # Get command from arguments
    if len(sys.argv) < 2:
        command = "status"
    else:
        command = sys.argv[1].lower()
    
    # Execute command
    if command in ["enable-choices", "enable_choices"]:
        enable_choices()
    elif command in ["disable-choices", "disable_choices"]:
        disable_choices()
    elif command in ["enable-tests", "enable_tests"]:
        enable_tests()
    elif command in ["disable-tests", "disable_tests"]:
        disable_tests()
    elif command in ["enable-parallel", "enable_parallel"]:
        enable_parallel()
    elif command in ["disable-parallel", "disable_parallel"]:
        disable_parallel()
    elif command == "status":
        show_status()
    elif command in ["help", "--help", "-h"]:
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        print("💡 Use 'help' to see available commands")
        show_status()

if __name__ == "__main__":
    main()
