# 🚀 Claude Hook - Supercharge Your Claude CLI

Transform your Claude CLI into an AI development powerhouse with intelligent automation hooks.

[![GitHub stars](https://img.shields.io/github/stars/bacoco/claude-hook.svg?style=social&label=Star)](https://github.com/bacoco/claude-hook)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ⚡ One-Line Install

```bash
curl -fsSL https://raw.githubusercontent.com/bacoco/claude-hook/main/install.sh | bash
```

## 🎯 What You Get

- **🎯 Smart Multiple Choice** - Automatic A/B/C options for complex questions
- **🧪 Enforced Testing** - Mandatory test creation and execution  
- **🔒 Security Guard** - Block dangerous operations automatically
- **⚡ Auto-Optimization** - Code formatting and linting on-the-fly
- **📚 Documentation Enforcer** - Ensure all functions are documented
- **💾 Git Backup System** - Intelligent branching for significant changes
- **📊 Usage Analytics** - Track your coding patterns
- **🎛️ Easy Controls** - Toggle any feature with `/enable-*` commands

## 🚀 Quick Start

1. **Install**: `curl -fsSL https://raw.githubusercontent.com/bacoco/claude-hook/main/install.sh | bash`
2. **Start Claude**: `claude`  
3. **Check status**: `/status`
4. **Customize**: `/enable-tests`, `/disable-choices`, etc.

## 📊 Example Usage

```
User: "How to optimize this function?"

Claude: 
**Option A:** Quick optimizations (variables, loops)
**Option B:** Balanced refactoring (structure, patterns)  
**Option C:** Complete rewrite (algorithms, architecture)

Which option would you prefer? (A/B/C)

User: "B"

Claude: [Implements balanced refactoring...]
[Creates optimized code]

🧪 TESTS REQUIRED - Creating and running tests...
🎨 AUTO-FORMATTING - Applying code style...  
📚 DOCS REQUIRED - Adding documentation...
✅ All tests pass! Code is ready.
```

## 🛠️ Manual Install

```bash
git clone https://github.com/bacoco/claude-hook.git
cd claude-hook
./install.sh
```

## 📱 Quick Commands

| Command | Description |
|---------|-------------|
| `/status` | Show current hook status |
| `/enable-choices` | Turn on A/B/C options |
| `/enable-tests` | Turn on mandatory testing |
| `/disable-tests` | Turn off testing |
| `/disable-choices` | Turn off choices |

## 🎛️ Features Control

All features can be toggled on/off:

```bash
# In Claude CLI
/enable-choices    # A/B/C options for complex questions
/disable-choices   # Turn off choice system

/enable-tests      # Mandatory test creation/execution  
/disable-tests     # Turn off test enforcement

/status           # Check what's currently enabled
```

## 🏗️ What Gets Installed

- **SessionStart Hook** - Injects choice system and context
- **PreToolUse Hooks** - Security guard, backup system, analytics
- **PostToolUse Hooks** - Test enforcement, optimization, documentation
- **Slash Commands** - Easy control commands
- **Analytics System** - Track your productivity patterns

## 📖 Documentation

- [Customization Guide](docs/CUSTOMIZATION.md) - Adapt to your workflow
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Fix common issues
- [Hook API Reference](docs/API.md) - Technical details

## 🔧 Requirements

- [Claude CLI](https://docs.anthropic.com/en/docs/claude-code) installed
- Python 3.6+
- Git (for backup features)

## 🤝 Contributing

Found a bug or want to add a feature? 

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## ⭐ Star This Repo

If this helps your workflow, please star the repo to help others discover it!

## 🙏 Credits

Created by [bacoco](https://github.com/bacoco) to supercharge Claude CLI development workflows.

---

**Ready to revolutionize your development experience?** ⚡

```bash
curl -fsSL https://raw.githubusercontent.com/bacoco/claude-hook/main/install.sh | bash
```
