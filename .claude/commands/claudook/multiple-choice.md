# Multiple Choice System

Automatically presents options for complex decisions

## Usage
Enable/disable the system:
```bash
# Enable
node .claude/hooks/claudook/toggle_controls.js enable-choices

# Disable  
node .claude/hooks/claudook/toggle_controls.js disable-choices
```

## Features
When enabled, Claude automatically:
- Detects complex decisions and questions
- Presents multiple implementation options
- Shows pros/cons for each approach
- Provides time estimates
- Waits for user selection (A/B/C)

## Example
```
You: "How should I handle user authentication?"

Claude: I can see multiple approaches:

**Option A: JWT with Redis Sessions**
- Pros: Scalable, stateless, secure
- Cons: More complex setup
- Time: ~30 minutes

**Option B: Simple Session Cookies**
- Pros: Easy to implement
- Cons: Less scalable  
- Time: ~15 minutes

**Option C: OAuth2 with Providers**
- Pros: No password management
- Cons: External dependency
- Time: ~45 minutes

Which would you prefer? (A/B/C)
```
