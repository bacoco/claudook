# Claudook - Local Enhancement for Claude Code

Install project-specific automation hooks that enhance Claude Code with intelligent features, without affecting your global Claude settings.

## ✨ Features

### 🎯 Multiple Choice System
Get A/B/C options for complex questions - Claude presents different approaches before implementation

### 🧪 Test Enforcement
Ensures all code modifications include tests - Claude is blocked until tests are created and pass

### 🔒 Security Protection
Blocks dangerous operations like `rm -rf /`, `curl | bash`, and protects sensitive files

### ⚡ Performance Optimization
Auto-formats and optimizes code using appropriate tools for each language

### 📚 Documentation Enforcement
Requires proper documentation for functions and important code sections

## 🚀 Installation (Local Only)

Claudook installs **locally in your project directory** - no system-wide changes!

```bash
# Install in current directory
curl -fsSL https://raw.githubusercontent.com/bacoco/claudook/main/install.sh | bash
```

Or clone and install:
```bash
git clone https://github.com/bacoco/claudook /tmp/claudook && \
  /tmp/claudook/install.sh && \
  rm -rf /tmp/claudook
```

### What Gets Installed

```
your-project/
├── .claude/
│   ├── hooks/claudook/     # Hook scripts
│   ├── commands/           # Slash commands
│   ├── settings.json       # Local settings
│   ├── choices_enabled     # Feature flag
│   └── tests_enabled       # Feature flag
└── CLAUDE.md              # Project config
```

## 📋 Commands

Use these in Claude when working in your project:

### Core Controls
- `/status` - Check hook status
- `/enable-choices` - Enable A/B/C options
- `/disable-choices` - Disable A/B/C options
- `/enable-tests` - Enable test enforcement
- `/disable-tests` - Disable test enforcement

### Parallel Execution (NEW)
- `/enable-parallel` - Enable parallel task execution
- `/disable-parallel` - Disable parallel task execution
- `/task-status` - View current task execution status

## 🔧 Direct Control

```bash
# From your project directory
python3 .claude/hooks/claudook/toggle_controls.py status
python3 .claude/hooks/claudook/toggle_controls.py enable-choices
python3 .claude/hooks/claudook/toggle_controls.py disable-choices
```

## 🗑️ Uninstall

Simply remove the `.claude` directory:
```bash
rm -rf .claude/
```

## 📝 Benefits of Local Installation

- ✅ **Project-specific** - Each project has its own configuration
- ✅ **No restart needed** - Works immediately
- ✅ **No system changes** - Doesn't touch `~/.claude/`
- ✅ **Easy cleanup** - Just delete `.claude/` folder
- ✅ **Version control** - Can commit `.claude/` with your project

## 🛠️ How It Works

Claudook uses Claude's hook system locally:
1. **SessionStart** - Loads project context
2. **PreToolUse** - Validates operations
3. **PostToolUse** - Enforces requirements

All hooks run from `.claude/hooks/claudook/` in your project.

## 📄 License

MIT

## 🌟 Support

- [GitHub Issues](https://github.com/bacoco/claudook/issues)
- Check `/status` after installation