#!/usr/bin/env python3
"""
Claudook - Security Guard
Blocks potentially dangerous operations before they execute.
"""
import json
import sys
import re
import os

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
    
    # Define dangerous command patterns
    dangerous_patterns = [
        # Destructive file operations
        (r'rm\s+-rf\s+/', "Recursive force delete from root directory"),
        (r'sudo\s+rm\s+-rf', "Sudo recursive force delete"),
        (r'rm\s+-rf\s+\*', "Recursive force delete with wildcard"),
        
        # Dangerous permissions
        (r'chmod\s+777\s+/', "Setting 777 permissions on root"),
        (r'chmod\s+-R\s+777', "Recursive 777 permissions"),
        
        # System modification
        (r'mkfs\.', "Filesystem formatting"),
        (r'fdisk\s+/dev/', "Disk partitioning"),
        (r'dd\s+if=.*of=/dev/', "Direct disk writing"),
        
        # Network security risks
        (r'curl.*\|\s*bash', "Piping curl output to bash"),
        (r'wget.*\|\s*sh', "Piping wget output to shell"),
        (r'curl.*\|\s*sudo\s+bash', "Piping to sudo bash"),
        
        # System control
        (r'shutdown|halt|reboot', "System shutdown commands"),
        (r'kill\s+-9\s+1', "Killing init process"),
        
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
