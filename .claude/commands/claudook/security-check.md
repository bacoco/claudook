# claudook/security-check

Run comprehensive security analysis on the current codebase.

## Usage
```bash
python3 .claude/hooks/claudook/security_guard.py --full-scan
```

## What it checks:
- Sensitive data exposure (API keys, passwords, tokens)
- SQL injection vulnerabilities
- XSS vulnerabilities
- Insecure dependencies
- File permission issues
- Authentication weaknesses
- Encryption problems

## Output
- Security score (0-100)
- List of vulnerabilities by severity (Critical, High, Medium, Low)
- Recommended fixes
- OWASP Top 10 compliance status