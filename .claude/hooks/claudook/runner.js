#!/usr/bin/env node

/**
 * Claudook Universal Runner - Solves all path issues!
 *
 * Can be called with:
 * - node .claude/hooks/claudook/runner.js <script> [args]
 * - npx .claude/hooks/claudook/runner.js <script> [args]
 *
 * Automatically finds and runs hooks from the correct location
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

function findClaudeRoot(dir = process.cwd()) {
  while (dir !== '/') {
    if (fs.existsSync(path.join(dir, '.claude'))) {
      return dir;
    }
    dir = path.dirname(dir);
  }
  return null;
}

const root = findClaudeRoot();
if (!root) {
  // Silent fail - no .claude directory
  process.exit(0);
}

const script = process.argv[2];
if (!script) {
  process.exit(0);
}

const scriptPath = path.join(root, '.claude', 'hooks', 'claudook', script);
if (!fs.existsSync(scriptPath)) {
  // Silent fail - script doesn't exist
  process.exit(0);
}

// Run Python script from project root
const proc = spawn('python3', [scriptPath, ...process.argv.slice(3)], {
  cwd: root,
  stdio: 'inherit',
  env: { ...process.env, CLAUDOOK_ROOT: root },
});

proc.on('error', () => process.exit(0));
proc.on('exit', (code) => process.exit(code || 0));
