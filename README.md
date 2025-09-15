# 🚀 Claudook - Transform Claude into Your AI Development Powerhouse

**Pure JavaScript. No Python Required.** Make Claude remember your project conventions, enforce quality standards, and work the way YOU want.

[![npm version](https://img.shields.io/npm/v/create-claudook.svg)](https://www.npmjs.com/package/create-claudook)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

## 🔥 Current Status

**All features are now ACTIVE and working:**
- 🟢 **Multiple Choice System**: ON - Claude offers A/B/C options for complex decisions
- 🟢 **Automatic Testing**: ON - Tests are mandatory after code changes
- 🟢 **Parallel Task Execution**: ON - Complex tasks run in parallel
- ✅ **Security Guard**: Always active - Blocks dangerous commands
- ✅ **Performance Optimizer**: Always active - Optimizes code automatically
- ✅ **Documentation Enforcer**: Always active - Keeps docs updated

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

### Prerequisites
- Node.js 14+
- npm (comes with Node.js)

### Quick Install (30 seconds)

#### Option 1: NPX (Recommended)
```bash
npx create-claudook
```

#### Option 2: Tell Claude
```
Install Claudook using npx create-claudook
```

#### Option 3: Global Install
```bash
npm install -g create-claudook
create-claudook
```

**That's it!** No configuration needed. Works immediately.

### What You'll See After Installation

```
🎉 Local Installation Complete!
==============================

📁 Installed in: /your-project/.claude/

🎯 Available Commands:
  /claudook/help           - Show all available commands
  /claudook/status         - Check current status
  /claudook/choices-enable  - Turn on A/B/C options
  /claudook/tests-enable    - Turn on mandatory testing

✨ Claudook is now active for this project!
```

### What Gets Installed

```
your-project/
├── package.json          # Updated with Claudook dependencies
├── CLAUDE.md            # Project configuration
└── .claude/
    ├── hooks/
    │   └── claudook/     # JavaScript automation scripts (ES modules)
    │       ├── security_guard.js
    │       ├── analytics_tracker.js
    │       ├── git_backup.js
    │       └── toggle_controls.js
    ├── commands/
    │   └── claudook/     # All slash commands
    ├── settings.json     # Hook configuration
    ├── choices_enabled   # Feature flag
    └── tests_enabled     # Feature flag
```

### Starting a New Session

When you start Claude after installation, you'll see:
```
🚀 Claudook Active [A/B/C + Tests]

📋 Quick Commands:
  /claudook/help     - Show all commands
  /claudook/status   - Check current status
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
- **Security**: `/claudook/security-enable`, `/claudook/security-disable`, `/claudook/security-check`
- **Analysis**: `/claudook/performance-check`, `/claudook/lint`
- **Config**: `/claudook/config-show`, `/claudook/config-reset`, `/claudook/update`

## 🔒 Security Features (Opt-In)

**By default, Claudook runs in minimal mode** to avoid blocking legitimate commands.

Advanced security features are **opt-in** because they can:
- Block commands in subdirectories
- Interfere with complex workflows
- Add overhead to every operation
- Cause false positives

### Enable Advanced Security
```bash
/claudook/security-enable
```

This activates:
- **Security Guard**: Blocks dangerous commands
- **Performance Optimizer**: Auto-optimizes code
- **Documentation Enforcer**: Ensures docs are updated
- **Git Backup**: Suggests backups before risky operations

### Disable If Needed
```bash
/claudook/security-disable
```

Returns to minimal, non-blocking mode.

### 🚨 Emergency Hook Control

If you need to disable ALL hooks immediately:

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

Claudook uses Claude's hook system with pure JavaScript:

1. **JavaScript Hooks** - All hooks are now Node.js scripts
2. **Automatic Path Resolution** - Works from any directory
3. **Event Interception** - Monitors Claude's tool usage
4. **Real-time Protection** - Blocks dangerous operations instantly

### Technical Architecture
```javascript
// Example: Security Guard Hook
const DANGEROUS_PATTERNS = [
  { pattern: /rm\s+-rf\s+\//, message: 'Attempting to delete root' },
  { pattern: /curl.*\|\s*(?:bash|sh)/, message: 'Piping untrusted scripts' }
];

// Automatically blocks dangerous commands
if (pattern.test(command)) {
  console.error('⛔ SECURITY BLOCK');
  process.exit(1);
}
```

No Python. No path issues. Just clean JavaScript.

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

Everything is customizable with JavaScript. Edit `.claude/hooks/claudook/*.js` to:
- Add your own security rules
- Define project-specific patterns
- Create custom hooks
- Set your testing requirements

### Running Tests
```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Watch mode for development
npm run test:watch
```

### Code Quality
```bash
# Format code
npm run format

# Lint code
npm run lint

# Full validation
npm run validate
```

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

## 🎉 MAJOR UPDATE: Now 100% JavaScript!

**No more Python dependency issues!** Claudook has been completely rewritten in JavaScript, solving all path resolution problems once and for all.

### What's New
- ✅ **Pure JavaScript hooks** - No Python required
- ✅ **npm/Node.js integration** - Use familiar JavaScript tools
- ✅ **Comprehensive test suite** - Jest tests with 100% coverage
- ✅ **Works from any directory** - No more "serpent qui se mord la queue" issues
- ✅ **Faster execution** - Native Node.js performance

## 🔧 Recent Improvements

### Latest Updates (2025-01-15) - JavaScript Edition
- **Hook Execution Fix**: All hooks now run through `python3` + `hook_runner.py` wrapper for robust execution
- **Path Resolution**: Hooks automatically resolve to project root, fixing "No such file" errors
- **Active Configuration**: Settings now properly activated via `.claude/settings.json`
- **Feature Toggles**: All features (choices, tests, parallel) now fully functional
- **Cross-Repository Safety**: Hooks handle directory changes and missing paths gracefully

### Previous Updates
- **Robust Path Resolution**: All hooks now work from any subdirectory
- **Session Folder Fix**: Task orchestration properly creates session folders with all files
- **Global Install Protection**: Install script prevents accidental global installation
- **Emergency Controls**: Quick disable/enable scripts for when hooks block work
- **Clean Uninstall**: Comprehensive uninstall scripts in main directory

### Known Issues Fixed
- ✅ Hooks failing with exit code 127 (/bin/sh execution)
- ✅ "No such file or directory" errors in subdirectories
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