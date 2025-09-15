#!/usr/bin/env python3
"""
Claudook - Smart Controller
Main controller for multiple choice system and test enforcement.
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


# Control files for toggling features
CHOICES_CONTROL = os.path.expanduser("~/.claude/choices_enabled")
TESTS_CONTROL = os.path.expanduser("~/.claude/tests_enabled")

def is_enabled(control_file):
    """Check if a feature is enabled by checking if its control file exists."""
    return os.path.exists(control_file)

def get_session_context():
    """Generate session context based on enabled features."""
    # Check enabled features
    choices_enabled = is_enabled(CHOICES_CONTROL)
    tests_enabled = is_enabled(TESTS_CONTROL)

    # Build feature status
    features = []
    if choices_enabled:
        features.append("✅ A/B/C")
    if tests_enabled:
        features.append("✅ Tests")

    lines = []

    # Claudook status line
    if features:
        lines.append(f"🚀 Claudook [{' • '.join(features)}] — /claudook/help for all commands")
    else:
        lines.append("🚀 Claudook Ready — /claudook/help to get started")

    # Quick toggles (show what's not enabled)
    quick_enables = []
    if not choices_enabled:
        quick_enables.append("/claudook/choices-enable")
    if not tests_enabled:
        quick_enables.append("/claudook/tests-enable")

    if quick_enables:
        lines.append(f"   Quick enable: {' • '.join(quick_enables)}")

    # If features are active, show what they do (very brief)
    if choices_enabled or tests_enabled:
        active = []
        if choices_enabled:
            active.append("A/B/C options")
        if tests_enabled:
            active.append("auto-tests")
        lines.append(f"   Active: {', '.join(active)} on all code changes")

    return "\n".join(lines)

def handle_post_tool_use():
    """Handle PostToolUse hook for test enforcement."""
    if not is_enabled(TESTS_CONTROL):
        sys.exit(0)  # Tests disabled, let it pass
    
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # Invalid JSON, skip
        
    tool_name = data.get("tool_name", "")
    file_path = data.get("tool_input", {}).get("file_path", "")
    
    # Define code file extensions
    code_exts = ['.py', '.js', '.ts', '.jsx', '.tsx', '.go', '.java', '.php', '.rb', '.cpp', '.c', '.cs', '.rs']
    is_code = any(file_path.endswith(ext) for ext in code_exts)
    is_test = any(word in file_path.lower() for word in ['test', 'spec', '__test__', '.test.', '.spec.'])
    
    if tool_name in ["Edit", "Write", "MultiEdit"] and is_code and not is_test:
        # Determine test command based on file extension
        test_info = {
            '.py': ('pytest', 'test_*.py'),
            '.js': ('npm test', '*.test.js'),
            '.ts': ('npm test', '*.test.ts'),
            '.jsx': ('npm test', '*.test.jsx'),
            '.tsx': ('npm test', '*.test.tsx'),
            '.go': ('go test', '*_test.go'),
            '.java': ('mvn test', '*Test.java'),
            '.php': ('phpunit', '*Test.php'),
            '.rb': ('rspec', '*_spec.rb'),
            '.rs': ('cargo test', '*_test.rs'),
            '.cpp': ('make test', '*_test.cpp'),
            '.c': ('make test', '*_test.c'),
            '.cs': ('dotnet test', '*Test.cs'),
        }
        
        ext = next((ext for ext in test_info.keys() if file_path.endswith(ext)), '.py')
        test_cmd, test_pattern = test_info[ext]
        
        mandatory_msg = f"""
⚠️ MANDATORY TESTS for {file_path}

🚫 BLOCKED - You cannot continue without:

1. 🏗️ CREATE tests ({test_pattern}):
   ✓ Unit tests for each function
   ✓ Error and edge case tests
   ✓ Input validation tests

2. ⚡ EXECUTE immediately:
   ✓ Command: {test_cmd}
   ✓ Verify ALL tests pass

3. 🔄 FIX in loop:
   ✓ If failure → fix the code
   ✓ Re-run tests
   ✓ Repeat until 100% green ✅

4. 📊 FINAL RESULT:
   ✓ All tests pass
   ✓ No errors/warnings
   ✓ Code validated and robust

💡 To disable: /disable-tests

YOU ARE BLOCKED until completing these steps.
        """.strip()
        
        output = {
            "decision": "block",
            "reason": mandatory_msg
        }
        print(json.dumps(output))
        sys.exit(2)

def main():
    """Main entry point for the smart controller."""
    if len(sys.argv) < 2:
        print("Usage: smart_controller.py [session-start|post-tool]", file=sys.stderr)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "session-start":
        # Handle SessionStart hook
        context = get_session_context()
        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context
            }
        }
        print(json.dumps(output))
        sys.exit(0)
    
    elif command == "post-tool":
        # Handle PostToolUse hook
        handle_post_tool_use()
    
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
