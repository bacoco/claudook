#!/bin/bash
# Quick script to re-enable Claudook hooks

echo "🟢 Re-enabling Claudook hooks..."

# Find project root
CURRENT_DIR=$(pwd)
while [ "$CURRENT_DIR" != "/" ]; do
    if [ -f "$CURRENT_DIR/.claude/settings.json.disabled" ]; then
        break
    fi
    CURRENT_DIR=$(dirname "$CURRENT_DIR")
done

if [ ! -f "$CURRENT_DIR/.claude/settings.json.disabled" ]; then
    echo "❌ No disabled settings found"
    exit 1
fi

# Restore settings.json
mv "$CURRENT_DIR/.claude/settings.json.disabled" "$CURRENT_DIR/.claude/settings.json" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Hooks re-enabled! (settings.json.disabled → settings.json)"
else
    echo "⚠️ Error restoring hooks"
fi