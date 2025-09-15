# Claude Hook Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### 1. "Claude CLI not found" Error
**Problem**: Installation script can't find Claude CLI.

**Solution**:
```bash
# Install Claude CLI first
npm install -g @anthropic-ai/claude-code

# Then retry installation
./install.sh
```

#### 2. "Python 3 required but not found"
**Problem**: Python 3 is not installed or not in PATH.

**Solution**:
```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt-get install python3

# Verify installation
python3 --version
```

#### 3. Installation Completes but Hooks Don't Work
**Problem**: Hooks are installed but not triggering in Claude.

**Solution**:
1. Run verification script:
   ```bash
   ./verify-installation.sh
   ```

2. Check settings.json was updated:
   ```bash
   grep "claude-hook" ~/.claude/settings.json
   ```

3. If missing, manually merge settings:
   ```bash
   python3 << EOF
   import json
   with open('.claude/settings-hook.json') as f:
       hooks = json.load(f)
   with open('~/.claude/settings.json') as f:
       settings = json.load(f)
   settings['hooks'].update(hooks['hooks'])
   with open('~/.claude/settings.json', 'w') as f:
       json.dump(settings, f, indent=2)
   EOF
   ```

### Feature Not Working

#### 1. A/B/C Choices Not Appearing
**Problem**: Complex questions don't trigger multiple choice options.

**Check**:
```bash
# Verify feature is enabled
ls ~/.claude/choices_enabled

# If missing, enable it
touch ~/.claude/choices_enabled

# Test with Claude
/status
```

**Test Question**: "How should I implement user authentication?"

#### 2. Test Enforcement Not Blocking
**Problem**: Code changes don't trigger mandatory testing.

**Check**:
```bash
# Verify feature is enabled
ls ~/.claude/tests_enabled

# If missing, enable it
touch ~/.claude/tests_enabled

# Check hook is registered
grep "smart_controller.py post-tool" ~/.claude/settings.json
```

#### 3. Security Guard Not Blocking Dangerous Commands
**Problem**: Dangerous commands like `rm -rf /` aren't blocked.

**Test**:
```bash
echo '{"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}' | \
  python3 ~/.claude/hooks/claude-hook/security_guard.py

# Should output blocking message with non-zero exit code
```

**Fix**:
```bash
# Ensure security guard is in PreToolUse hooks
grep "security_guard" ~/.claude/settings.json

# Check file permissions
chmod +x ~/.claude/hooks/claude-hook/security_guard.py
```

### Command Issues

#### 1. "/status command not found"
**Problem**: Slash commands not recognized in Claude CLI.

**Solution**:
```bash
# Check command files exist
ls ~/.claude/commands/

# If missing, copy them
cp -r .claude/commands/* ~/.claude/commands/

# Restart Claude CLI
```

#### 2. Commands Run but Don't Work
**Problem**: Commands execute but don't change settings.

**Check**:
```bash
# Test directly
python3 ~/.claude/hooks/claude-hook/toggle_controls.py enable-choices

# Check control file was created
ls ~/.claude/choices_enabled
```

### Hook Errors

#### 1. "Permission denied" When Running Hooks
**Problem**: Hook scripts aren't executable.

**Solution**:
```bash
chmod +x ~/.claude/hooks/claude-hook/*.py
```

#### 2. JSON Output Errors
**Problem**: Hooks fail with JSON parsing errors.

**Test**:
```bash
# Test hook output
python3 ~/.claude/hooks/claude-hook/smart_controller.py session-start | python3 -m json.tool

# Should show valid JSON with hookSpecificOutput key
```

#### 3. Hook Timeout Issues
**Problem**: Hooks take too long and timeout.

**Check**:
- Ensure hooks don't have infinite loops
- Check network-dependent hooks have timeouts
- Verify Python dependencies are installed

### Performance Issues

#### 1. Claude CLI Slow After Installation
**Problem**: Hooks causing performance degradation.

**Temporary Fix**:
```bash
# Disable non-critical features
/disable-tests
/disable-choices

# Or temporarily rename settings
mv ~/.claude/settings.json ~/.claude/settings.json.backup
```

#### 2. High CPU Usage
**Problem**: Hooks consuming excessive resources.

**Debug**:
```bash
# Monitor hook execution
time python3 ~/.claude/hooks/claude-hook/analytics_tracker.py

# Check for runaway processes
ps aux | grep python | grep claude-hook
```

### Complete Reset

If all else fails, perform a complete reinstall:

```bash
# 1. Backup current settings
cp ~/.claude/settings.json ~/.claude/settings.json.backup.$(date +%s)

# 2. Remove all Claude Hook files
rm -rf ~/.claude/hooks/claude-hook/
rm ~/.claude/choices_enabled ~/.claude/tests_enabled
rm ~/.claude/commands/{status,enable-*,disable-*}.md

# 3. Clean settings.json (remove claudook references)
python3 << EOF
import json
with open('~/.claude/settings.json') as f:
    settings = json.load(f)
# Remove claude-hook hooks
for event in settings.get('hooks', {}):
    settings['hooks'][event] = [
        h for h in settings['hooks'][event]
        if 'claude-hook' not in str(h)
    ]
with open('~/.claude/settings.json', 'w') as f:
    json.dump(settings, f, indent=2)
EOF

# 4. Reinstall fresh
./install.sh

# 5. Verify
./verify-installation.sh
```

## Getting Help

### Debug Information to Collect

When reporting issues, include:

1. **System Info**:
   ```bash
   uname -a
   python3 --version
   claude --version
   ```

2. **Installation Status**:
   ```bash
   ./verify-installation.sh
   ```

3. **Hook Test Results**:
   ```bash
   python3 tests/test_all_hooks.py
   ```

4. **Settings Snapshot**:
   ```bash
   grep -A5 -B5 "claude-hook" ~/.claude/settings.json
   ```

### Support Channels

- **GitHub Issues**: https://github.com/bacoco/claude-hook/issues
- **Documentation**: Check `docs/` directory
- **Quick Test**: Run `./verify-installation.sh` first

## Prevention Tips

1. **Always verify after installation**:
   ```bash
   ./verify-installation.sh
   ```

2. **Test features individually**:
   ```bash
   /status
   /enable-choices
   # Test with a complex question
   /disable-choices
   ```

3. **Keep backups**:
   ```bash
   cp ~/.claude/settings.json ~/.claude/settings.json.backup
   ```

4. **Update regularly**:
   ```bash
   git pull origin main
   ./install.sh
   ```

## FAQ

**Q: Can I use Claude Hook with other Claude extensions?**
A: Yes, the `claude-hook` namespace prevents conflicts.

**Q: Will uninstalling break my Claude CLI?**
A: No, it only removes the hook additions.

**Q: Can I customize which features are enabled by default?**
A: Yes, modify the install.sh script before running.

**Q: Do hooks work with all Claude models?**
A: Yes, hooks work at the CLI level, not model level.

**Q: Can I add my own custom hooks?**
A: Yes, add them to `.claude/hooks/claude-hook/` and register in settings.