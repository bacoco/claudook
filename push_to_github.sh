#!/bin/bash
# Commands to push to your GitHub repository

echo "🚀 Initializing and pushing to GitHub repository..."

# Initialize git repository
git init

# Add GitHub repository as origin
git remote add origin https://github.com/bacoco/claude-hook.git

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Claude Hook superpowers

✨ Features:
- 🎯 Smart multiple choice system (A/B/C options)
- 🧪 Automatic test enforcement
- 🔒 Security guard against dangerous operations
- ⚡ Performance optimizer with auto-formatting
- 📚 Documentation enforcer
- 💾 Intelligent Git backup system
- 📊 Usage analytics tracker
- 🎛️ Easy on/off controls

🚀 One-line install: curl -fsSL https://raw.githubusercontent.com/bacoco/claude-hook/main/install.sh | bash"

# Push to GitHub
git branch -M main
git push -u origin main

echo ""
echo "✅ Repository successfully pushed to GitHub!"
echo "🌐 View at: https://github.com/bacoco/claude-hook"
echo ""
echo "🎯 Users can now install with:"
echo "curl -fsSL https://raw.githubusercontent.com/bacoco/claude-hook/main/install.sh | bash"
