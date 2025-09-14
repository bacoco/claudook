#!/bin/bash
# Push script for master-claude-hook repository

cd /Users/loic/develop/master-claude-hook

echo "🚀 Pushing Claude Hook to GitHub..."
echo "📁 Working in: $(pwd)"
echo ""

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git remote add origin https://github.com/bacoco/claude-hook.git
fi

# Add all files
echo "📝 Adding all files..."
git add .

# Create commit
echo "💾 Creating commit..."
git commit -m "🚀 Initial commit: Claude Hook superpowers

✨ Features:
- 🎯 Smart multiple choice system (A/B/C options)
- 🧪 Automatic test enforcement
- 🔒 Security guard against dangerous operations
- ⚡ Performance optimizer with auto-formatting
- 📚 Documentation enforcer
- 💾 Intelligent Git backup system
- 📊 Usage analytics tracker
- 🎛️ Easy on/off controls

🎯 One-line install:
curl -fsSL https://raw.githubusercontent.com/bacoco/claude-hook/main/install.sh | bash

📚 Complete documentation and troubleshooting guides included
🔧 Easy customization and team deployment ready"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo "🌐 Repository: https://github.com/bacoco/claude-hook"
echo ""
echo "🎯 Users can now install with:"
echo "curl -fsSL https://raw.githubusercontent.com/bacoco/claude-hook/main/install.sh | bash"
echo ""
echo "💡 Or tell Claude:"
echo "'Install claude-hook from https://github.com/bacoco/claude-hook'"
