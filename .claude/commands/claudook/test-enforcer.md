# Test Enforcer

Mandatory test creation after code modifications

## Usage
Enable/disable enforcement:
```bash
# Enable
node .claude/hooks/claudook/toggle_controls.js enable-tests

# Disable
node .claude/hooks/claudook/toggle_controls.js disable-tests
```

## Features
When enabled:
- Blocks after ANY code modification
- Requires test creation before continuing
- Ensures all tests pass
- Tracks modified files
- Validates test coverage

## Enforcement Flow
```
Code modified → 🚫 BLOCKED
     ↓
Create unit tests
     ↓
Create integration tests
     ↓
Run all tests
     ↓
Tests pass → ✅ Continue
```

## Example
```
You: "Add new login function"
Claude: *implements login function*

🚫 TEST ENFORCEMENT ACTIVE
━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Code modifications detected!
📝 You must create and run tests before continuing.

Required actions:
1. ✍️ Create unit tests
2. ✍️ Create integration tests  
3. ▶️ Run all tests
4. ✅ All tests must pass

Modified file: auth/login.js
━━━━━━━━━━━━━━━━━━━━━━━━

Claude: *creates comprehensive tests*
Claude: *runs tests*
✅ Tests executed - enforcement satisfied
```
