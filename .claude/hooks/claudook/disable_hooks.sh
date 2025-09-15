#!/bin/bash
# Quick script to disable Claudook hooks temporarily

echo "🔴 Disabling Claudook hooks..."

# Find project root
CURRENT_DIR=$(pwd)
while [ "$CURRENT_DIR" != "/" ]; do
    if [ -f "$CURRENT_DIR/.claude/settings.json" ]; then
        break
    fi
    CURRENT_DIR=$(dirname "$CURRENT_DIR")
done

if [ ! -f "$CURRENT_DIR/.claude/settings.json" ]; then
    echo "❌ No .claude/settings.json found"
    exit 1
fi

# Rename settings.json to disable hooks
mv "$CURRENT_DIR/.claude/settings.json" "$CURRENT_DIR/.claude/settings.json.disabled" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Hooks disabled! (settings.json → settings.json.disabled)"
    echo "To re-enable: ./claude/hooks/claudook/enable_hooks.sh"
else
    echo "⚠️ Hooks already disabled or error occurred"
fi