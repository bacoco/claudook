#!/usr/bin/env python3
"""
Claudook - Security Guard
Blocks potentially dangerous operations before they execute.
"""
import json
import sys
import re
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

def check_bash_command_security(command):
    """Check if a bash command is potentially dangerous."""
    if not command:
        return None

    # First, check for safe development patterns (always allow these)
    safe_patterns = [
        r'python3?\s+',      # Python commands
        r'node\s+',          # Node commands
        r'npm\s+',           # NPM commands
        r'yarn\s+',          # Yarn commands
        r'git\s+',           # Git commands
        r'docker\s+',        # Docker commands
        r'cd\s+',            # Directory changes
        r'ls\s+',            # List files
        r'cat\s+',           # View files
        r'grep\s+',          # Search files
        r'find\s+',          # Find files
        r'mkdir\s+',         # Create directories
        r'touch\s+',         # Create files
        r'echo\s+',          # Echo commands
        r'black\s+',         # Code formatting
        r'isort\s+',         # Import sorting
        r'pytest\s+',        # Testing
        r'./[^/]*\s',        # Local executables
    ]

    for safe_pattern in safe_patterns:
        if re.match(safe_pattern, command.strip()):
            return None  # Command is safe, don't block

    # Only block EXTREMELY dangerous command patterns
    dangerous_patterns = [
        # CRITICAL: Root filesystem destruction
        (r'rm\s+-rf\s+/\s*$', "Deleting root filesystem"),
        (r'rm\s+-rf\s+/\*', "Deleting all root contents"),
        (r'sudo\s+rm\s+-rf\s+/', "Sudo deletion of system files"),

        # CRITICAL: System destruction
        (r'mkfs\.', "Filesystem formatting"),
        (r'fdisk\s+/dev/sd[a-z]', "Partitioning main drives"),
        (r'dd\s+if=.*of=/dev/sd[a-z]\s', "Writing to main drive"),

        # CRITICAL: Remote code execution from untrusted sources (but not curl from GitHub)
        (r'curl\s+(?!.*github\.com).*\|\s*sudo\s+bash', "Sudo execution of remote script from untrusted source"),
        
        # Fork bombs and resource abuse  
        (r':(){ :|:& };:', "Fork bomb"),
        (r'while\s+true.*done.*&', "Infinite background loop"),
        
        # Suspicious background processes
        (r'nohup.*&.*>/dev/null', "Hidden background process"),
        (r'>\s*/dev/null\s+2>&1.*&', "Silent background process"),
    ]
    
    for pattern, description in dangerous_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            return description
    
    return None

def check_file_security(file_path):
    """Check if file path is sensitive."""
    if not file_path:
        return None
    
    # Define sensitive file patterns
    sensitive_patterns = [
        # Credential files
        (".env", "Environment variables file"),
        (".npmrc", "NPM configuration"),
        (".pypirc", "PyPI configuration"), 
        ("credentials", "Credentials file"),
        
        # SSH and security
        (".ssh/", "SSH configuration directory"),
        ("id_rsa", "SSH private key"),
        ("id_dsa", "SSH private key"),
        ("authorized_keys", "SSH authorized keys"),
        
        # System files
        ("passwd", "System password file"),
        ("shadow", "System shadow file"),
        ("sudoers", "Sudo configuration"),
        ("/etc/", "System configuration directory"),
        
        # Cloud credentials
        (".aws/credentials", "AWS credentials"),
        (".gcp/", "Google Cloud credentials"),
        (".azure/", "Azure credentials"),
        
        # Application secrets
        ("secret", "Secrets file"),
        ("token", "Token file"),
        (".cert", "Certificate file"),
        (".key", "Private key file"),
    ]
    
    for pattern, description in sensitive_patterns:
        if pattern in file_path.lower():
            return description
    
    return None

def main():
    """Main security guard logic."""
    data = load_hook_data()
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    
    # Check bash commands
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        threat = check_bash_command_security(command)
        
        if threat:
            output = {
                "decision": "block",
                "reason": f"""🚨 DANGEROUS COMMAND BLOCKED

Command: {command}
Risk: {threat}

⚠️ This command could cause system damage or security breach.

🛡️ Security measures active to protect your system.

💡 If you absolutely need this command:
   1. Review the command carefully
   2. Consider safer alternatives
   3. Use /override-security if truly necessary
"""
            }
            print(json.dumps(output))
            sys.exit(2)
    
    # Check file operations
    elif tool_name in ["Edit", "Write"]:
        file_path = tool_input.get("file_path", "")
        threat = check_file_security(file_path)
        
        if threat:
            output = {
                "decision": "block",
                "reason": f"""🔐 SENSITIVE FILE BLOCKED

File: {file_path}
Type: {threat}

⚠️ Modification blocked for security reasons.

🛡️ This file may contain sensitive information like:
   • Passwords or API keys
   • System configuration
   • Private certificates
   • Access credentials

💡 If you need to modify this file:
   1. Ensure you understand the security implications
   2. Make a backup first
   3. Use /override-security if necessary
"""
            }
            print(json.dumps(output))
            sys.exit(2)
    
    # Allow operation if no threats detected
    sys.exit(0)

if __name__ == "__main__":
    main()
