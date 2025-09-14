# Troubleshooting Guide

Solutions for common Claude Hook issues and problems.

## Installation Issues

### Claude CLI Not Found

**Error**: `❌ Claude CLI not found`

**Solution**:
```bash
# Install Claude CLI
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version
```

**Alternative**: Use the native installer:
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

### Python Not Found

**Error**: `❌ Python 3 required but not found`

**Solutions**:
```bash
# macOS
brew install python3

# Ubuntu/Debian  
sudo apt update && sudo apt install python3

# Windows (use WSL or install Python directly)
python --version  # Should be 3.6+
```

### Permission Denied

**Error**: `Permission denied: ~/.claude/hooks/script.py`

**Solution**:
```bash
# Fix permissions
chmod +x ~/.claude/hooks/*.py

# Or re-run installation
curl -fsSL https://raw.githubusercontent.com/bacoco/claude-hook/main/install.sh | bash
```

## Hook Execution Issues

### Hooks Not Running

**Symptoms**: No hook effects visible in Claude CLI

**Debug Steps**:

1. **Check hook configuration**:
   ```bash
   # In Claude CLI
   /hooks
   # Should show your installed hooks
   ```

2. **Verify settings.json**:
   ```bash
   cat ~/.claude/settings.json
   # Should contain hook definitions
   ```

3. **Test hooks manually**:
   ```bash
   python3 ~/.claude/hooks/smart_controller.py session-start
   # Should output JSON
   ```

4. **Check file permissions**:
   ```bash
   ls -la ~/.claude/hooks/
   # All .py files should be executable (+x)
   ```

### Hook Syntax Errors

**Error**: `SyntaxError` or `ImportError` in hook scripts

**Solution**:
```bash
# Test Python syntax
python3 -m py_compile ~/.claude/hooks/smart_controller.py

# Check for missing modules
python3 -c "import json, sys, os"
```

### JSON Parse Errors

**Error**: `JSONDecodeError` in hook output

**Debug**:
```bash
# Test hook output
echo '{"tool_name":"Edit","tool_input":{"file_path":"test.py"}}' | \
python3 ~/.claude/hooks/smart_controller.py post-tool
```

**Fix**: Ensure hooks always output valid JSON:
```python
# Always wrap output in try/catch
try:
    output = {"key": "value"}
    print(json.dumps(output))
except Exception:
    print("{}")  # Empty JSON as fallback
```

## Feature Issues

### Multiple Choices Not Working

**Check**:
```bash
# Verify choices are enabled
ls ~/.claude/choices_enabled
# File should exist

# Test status
python3 ~/.claude/hooks/toggle_controls.py status
```

**Fix**:
```bash
# Re-enable choices
/enable-choices
# or
python3 ~/.claude/hooks/toggle_controls.py enable-choices
```

### Tests Not Being Enforced

**Check**:
```bash
# Verify tests are enabled
ls ~/.claude/tests_enabled
# File should exist

# Check PostToolUse hooks
grep -A 10 "PostToolUse" ~/.claude/settings.json
```

**Fix**:
```bash
# Re-enable tests
/enable-tests

# Check hook matcher
# Should include "Edit|Write|MultiEdit"
```

### Security Guard Too Strict

**Issue**: Legitimate commands being blocked

**Solutions**:

1. **Temporary override**:
   ```bash
   # Add override flag (modify security_guard.py)
   export CLAUDE_SECURITY_OVERRIDE=true
   ```

2. **Customize patterns**:
   ```python
   # In security_guard.py, modify dangerous_patterns
   dangerous_patterns = [
       # Comment out overly strict patterns
       # (r'your-pattern', "description"),
   ]
   ```

3. **Whitelist approach**:
   ```python
   # Add safe command whitelist
   safe_commands = ['your-safe-command', 'another-command']
   if any(cmd in command for cmd in safe_commands):
       sys.exit(0)  # Allow command
   ```

### Performance Optimizer Conflicts

**Issue**: Conflicts with existing formatters

**Solution**:
```python
# In perf_optimizer.py, customize for your setup
tools_map = {
    '.py': {
        'formatter': 'your-preferred-formatter',
        'linter': 'your-preferred-linter',
    }
}
```

## Claude CLI Integration Issues

### Hooks Menu Empty

**Problem**: `/hooks` command shows no hooks

**Solution**:
```bash
# Check if settings.json exists and is valid
python3 -c "import json; print(json.load(open('$HOME/.claude/settings.json')))"

# Re-run installation
curl -fsSL https://raw.githubusercontent.com/bacoco/claude-hook/main/install.sh | bash
```

### Settings Not Persisting

**Problem**: Hook settings reset after restart

**Check**:
```bash
# Verify settings location
ls -la ~/.claude/settings.json

# Check for backup files
ls ~/.claude/settings.json.backup.*
```

**Fix**:
```bash
# Restore from backup if needed
cp ~/.claude/settings.json.backup.TIMESTAMP ~/.claude/settings.json

# Re-run installation
./install.sh
```

### Slash Commands Not Working

**Problem**: `/status`, `/enable-choices` etc. not recognized

**Solution**:
```bash
# Check commands directory
ls ~/.claude/commands/

# Should contain: enable-choices.md, disable-choices.md, etc.

# Re-install commands
cp commands/*.md ~/.claude/commands/
```

## Performance Issues

### Hooks Running Slowly

**Symptoms**: Noticeable delay in Claude CLI responses

**Solutions**:

1. **Disable heavy analytics**:
   ```python
   # In analytics_tracker.py
   if os.environ.get('CLAUDE_FAST_MODE'):
       sys.exit(0)  # Skip analytics
   ```

2. **Optimize hook scripts**:
   ```python
   # Add early exits
   if not should_process_this_file(file_path):
       sys.exit(0)
   ```

3. **Reduce git operations**:
   ```python
   # In git_backup.py, cache git status
   _git_status_cache = None
   ```

### High Memory Usage

**Solution**:
```python
# In analytics_tracker.py
def cleanup_old_files():
    # Reduce retention period
    cutoff_date = date.today() - timedelta(days=7)  # Reduced from 30
```

## Git Integration Issues

### Git Commands Failing

**Error**: Git operations in `git_backup.py` failing

**Debug**:
```bash
# Test git in current directory
git status
git branch --show-current

# Check git configuration
git config --list
```

**Fix**:
```python
# In git_backup.py, add better error handling
def run_git_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=5)
        return result.stdout.strip() if result.returncode == 0 else None
    except:
        return None
```

### Backup Suggestions Not Appearing

**Check**:
```bash
# Verify you're in a git repository
git rev-parse --git-dir

# Check if backup suggestions are printed
python3 ~/.claude/hooks/git_backup.py < test_data.json
```

## Analytics Issues

### Analytics Files Growing Too Large

**Solution**:
```bash
# Clear old analytics
rm ~/.claude/analytics/daily_*.json
rm ~/.claude/analytics/events.jsonl

# Or configure cleanup
export CLAUDE_ANALYTICS_RETENTION_DAYS=7
```

### Analytics Directory Permissions

**Error**: Cannot write to analytics directory

**Fix**:
```bash
# Fix permissions
chmod 755 ~/.claude/analytics
chmod 644 ~/.claude/analytics/*
```

## Environment-Specific Issues

### Windows/WSL Issues

**Common problems**:
- Path separators (`\` vs `/`)
- Line ending differences (CRLF vs LF)
- Permission model differences

**Solutions**:
```bash
# Convert line endings
dos2unix ~/.claude/hooks/*.py

# Fix paths in hooks
sed -i 's/\\/\//g' ~/.claude/hooks/*.py
```

### macOS Permissions

**Error**: macOS blocking hook execution

**Solution**:
```bash
# Allow execution
xattr -dr com.apple.quarantine ~/.claude/hooks/

# Or re-download and install
curl -fsSL https://raw.githubusercontent.com/bacoco/claude-hook/main/install.sh | bash
```

## Debug Mode

### Enable Debug Output

Add to your shell configuration:
```bash
export CLAUDE_HOOK_DEBUG=true
export CLAUDE_HOOK_VERBOSE=true
```

### Manual Hook Testing

```bash
# Test session start
python3 ~/.claude/hooks/smart_controller.py session-start

# Test post tool use
echo '{"tool_name":"Edit","tool_input":{"file_path":"test.py","content":"print(hello)"}}' | \
python3 ~/.claude/hooks/smart_controller.py post-tool

# Test security guard
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | \
python3 ~/.claude/hooks/security_guard.py
```

### Hook Output Inspection

```bash
# Capture hook output
echo '{"tool_name":"Edit","tool_input":{"file_path":"test.py"}}' | \
python3 ~/.claude/hooks/doc_enforcer.py 2>&1 | tee hook_output.log
```

## Getting Help

If you're still having issues:

1. **Check GitHub Issues**: [github.com/bacoco/claude-hook/issues](https://github.com/bacoco/claude-hook/issues)

2. **Create a Bug Report** with:
   - Your operating system
   - Claude CLI version (`claude --version`)
   - Python version (`python3 --version`)
   - Hook output/error messages
   - Steps to reproduce

3. **Join Discussions**: Share your issue in GitHub Discussions

4. **Emergency Reset**:
   ```bash
   # Complete reset
   mv ~/.claude ~/.claude.backup
   curl -fsSL https://raw.githubusercontent.com/bacoco/claude-hook/main/install.sh | bash
   ```

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `FileNotFoundError: python3` | Python not installed | Install Python 3.6+ |
| `JSONDecodeError` | Invalid JSON in hook | Check hook script syntax |
| `PermissionError` | File permissions | `chmod +x ~/.claude/hooks/*.py` |
| `ModuleNotFoundError` | Missing Python modules | Use system Python, not venv |
| `Hook timeout` | Hook taking too long | Add timeout handling |
| `Settings not found` | Missing configuration | Re-run `install.sh` |

---

**Still stuck?** Open an issue on GitHub with details! 🚀
