# Claude Hook - Enhance Claude Code with Automation Superpowers

Claude Hook is a comprehensive automation system that enhances Claude Code (claude.ai/code) with intelligent workflows, multiple choice options, test enforcement, security protection, and performance optimization.

## ✨ Features

### 🎯 Multiple Choice System
Automatically get A/B/C options for complex questions:
- **Option A**: Quick/simple solution
- **Option B**: Balanced approach
- **Option C**: Advanced implementation

### 🧪 Test Enforcement
After code modifications, Claude is blocked until:
- Comprehensive tests are created
- Tests are executed and pass
- Code quality is verified

### 🔒 Security Protection
Blocks dangerous operations before execution:
- Destructive file operations (`rm -rf /`)
- Suspicious network commands (`curl | bash`)
- System modifications
- Sensitive file access

### ⚡ Performance Optimization
Automatic code improvements:
- Code formatting (Black, Prettier, etc.)
- Linting and style compliance
- Import organization
- Performance suggestions

### 📚 Documentation Enforcement
Ensures all code is documented:
- Python docstrings
- JSDoc comments
- Function documentation
- Parameter descriptions

## 🚀 Quick Installation

### Method 1: One-Line Installation (Recommended)
```bash
# Download and run installer directly (no clone needed)
curl -fsSL https://raw.githubusercontent.com/bacoco/claude-hook/main/install.sh | bash
```

### Method 2: Temporary Clone & Install
```bash
# Clone to temp directory, install, and clean up
git clone https://github.com/bacoco/claude-hook /tmp/claude-hook && \
  /tmp/claude-hook/install.sh && \
  rm -rf /tmp/claude-hook
```

### Method 3: Let Claude Install It
Simply tell Claude:
```
Install Claude Hook from https://github.com/bacoco/claude-hook
```

**⚠️ IMPORTANT:** After installation, you must **restart Claude CLI** for changes to take effect!

## 📋 Commands

Once installed, use these commands in Claude CLI:

- `/status` - Check current hook status
- `/enable-choices` - Enable A/B/C options
- `/disable-choices` - Disable A/B/C options
- `/enable-tests` - Enable test enforcement
- `/disable-tests` - Disable test enforcement

## 🔧 Project Structure

```
claude-hook/
├── .claude/
│   ├── hooks/claude-hook/    # All hook scripts
│   ├── commands/              # Slash commands
│   └── settings-hook.json     # Hook configuration
├── install.sh                 # Installation script
├── verify-installation.sh     # Verification script
├── tests/                     # Test suite
└── docs/                      # Documentation
```

## ✅ Verify Installation

After installation:

1. **Restart Claude CLI** (exit and run `claude` again)
2. Test with `/status` command
3. Ask a complex question to see A/B/C choices in action

```bash
# After restart, in Claude CLI:
/status
```

## 🧪 What Gets Installed

Only the essential files are installed to `~/.claude/`:
- **8 hook scripts** in `~/.claude/hooks/claude-hook/`
- **5 commands** in `~/.claude/commands/`
- **Settings merged** into `~/.claude/settings.json`

No documentation, tests, or other files are copied to your system.

## 📚 Documentation

- [API Reference](docs/API.md) - Hook API documentation
- [Customization Guide](docs/CUSTOMIZATION.md) - How to customize hooks
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions
- [Claude Integration](CLAUDE.md) - How Claude Code uses these hooks

## 🛠️ How It Works

1. **Hooks** integrate with Claude's event system (SessionStart, PreToolUse, PostToolUse)
2. **Commands** are registered in `~/.claude/commands/`
3. **Settings** are merged into `~/.claude/settings.json`
4. **Features** are controlled via toggle files

## 🎛️ Customization

### Add Your Own Hooks

1. Create a Python script in `.claude/hooks/claude-hook/`
2. Register it in `.claude/settings-hook.json`
3. Add a command in `.claude/commands/`

### Modify Behavior

- Edit hook scripts directly
- Adjust patterns in `security_guard.py`
- Customize prompts in `smart_controller.py`

## 🔍 Troubleshooting

If hooks aren't working:

1. Run `./verify-installation.sh`
2. Check `/status` in Claude CLI
3. See [Troubleshooting Guide](docs/TROUBLESHOOTING.md)

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Test your changes
4. Submit a pull request

## 🌟 Support

- **Issues**: [GitHub Issues](https://github.com/bacoco/claude-hook/issues)
- **Documentation**: Check the `docs/` directory
- **Quick Test**: Run `./verify-installation.sh`

---

**Ready to supercharge your Claude Code experience?** Run `./install.sh` and start coding with superpowers! 🚀