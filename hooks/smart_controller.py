#!/usr/bin/env python3
"""
Claude Hook - Smart Controller
Main controller for multiple choice system and test enforcement.
"""
import json
import sys
import os

# Control files for toggling features
CHOICES_CONTROL = os.path.expanduser("~/.claude/choices_enabled")
TESTS_CONTROL = os.path.expanduser("~/.claude/tests_enabled")

def is_enabled(control_file):
    """Check if a feature is enabled by checking if its control file exists."""
    return os.path.exists(control_file)

def get_session_context():
    """Generate session context based on enabled features."""
    context_parts = []
    
    # 1. Multiple Choice System
    if is_enabled(CHOICES_CONTROL):
        context_parts.append("""
🎯 MULTIPLE CHOICE MODE ACTIVE:
When my question could have multiple valid approaches, systematically propose:
• **Option A:** [quick/simple solution]
• **Option B:** [balanced approach] 
• **Option C:** [advanced/complete solution]

Then wait for my selection (A/B/C) before developing.
If obvious answer exists, respond directly.
        """.strip())
    
    # 2. Automatic Testing System
    if is_enabled(TESTS_CONTROL):
        context_parts.append("""
🧪 AUTOMATIC TESTING ACTIVE:
After EVERY code modification, you MUST automatically:
1. Create appropriate unit tests
2. Execute them immediately
3. Fix and iterate until they pass
No exceptions - tests are mandatory for all code.
        """.strip())
    
    # 3. Available Controls
    context_parts.append("""
📋 AVAILABLE CONTROLS:
- /enable-choices : Activate multiple choice system
- /disable-choices : Deactivate multiple choice system
- /enable-tests : Activate automatic testing
- /disable-tests : Deactivate automatic testing
- /status : Check current hook status
    """.strip())
    
    return "\n\n".join(context_parts)

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
