#!/usr/bin/env python3
"""
Claudook Hook Runner
Trouve automatiquement le dossier .claude/ et lance le bon hook
"""
import sys
import os
import subprocess
from pathlib import Path

def find_claude_root():
    """Trouve le dossier racine contenant .claude/"""
    current = Path.cwd().resolve()

    # Cherche en remontant l'arbre des dossiers
    for path in [current] + list(current.parents):
        if (path / ".claude").is_dir():
            return path

    # Fallback: si on est dans .claude/hooks/claudook
    if current.name == "claudook" and current.parent.name == "hooks":
        return current.parent.parent.parent

    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: hook_runner.py <hook_script> [args...]", file=sys.stderr)
        sys.exit(1)

    hook_script = sys.argv[1]
    hook_args = sys.argv[2:] if len(sys.argv) > 2 else []

    # Trouve le dossier racine
    claude_root = find_claude_root()
    if not claude_root:
        print("ERROR: Cannot find .claude directory", file=sys.stderr)
        sys.exit(1)

    # Construit le chemin vers le hook
    hook_path = claude_root / ".claude" / "hooks" / "claudook" / hook_script

    if not hook_path.exists():
        print(f"ERROR: Hook script not found: {hook_path}", file=sys.stderr)
        sys.exit(1)

    # Change vers le dossier racine pour que le hook trouve les bons chemins
    os.chdir(claude_root)

    # Lance le hook avec python3
    cmd = ["python3", str(hook_path)] + hook_args
    try:
        result = subprocess.run(cmd, capture_output=False)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"ERROR: Failed to run hook: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()