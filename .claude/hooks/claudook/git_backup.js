#!/usr/bin/env node

/**
 * Git Backup Suggester - JavaScript Version
 * Suggests backups before risky operations
 */

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

function findProjectRoot(dir = process.cwd()) {
  while (dir !== '/') {
    if (fs.existsSync(path.join(dir, '.claude'))) {
      return dir;
    }
    dir = path.dirname(dir);
  }
  return null;
}

function checkGitStatus() {
  try {
    const root = findProjectRoot();
    if (!root) return null;

    // Check if it's a git repo
    const gitDir = path.join(root, '.git');
    if (!fs.existsSync(gitDir)) return null;

    // Get git status
    const status = execSync('git status --porcelain', { cwd: root, encoding: 'utf8' });
    return status.trim().length > 0;
  } catch (e) {
    return null;
  }
}

function suggestBackup(input) {
  try {
    const data = JSON.parse(input);

    // Check for risky operations
    const riskyOperations = ['Write', 'Edit', 'MultiEdit'];
    if (!riskyOperations.includes(data.tool_name)) {
      process.exit(0);
    }

    // Check if there are uncommitted changes
    const hasChanges = checkGitStatus();
    if (hasChanges) {
      console.log('💡 Git Backup Reminder:');
      console.log('You have uncommitted changes. Consider:');
      console.log("- git add . && git commit -m 'Backup before changes'");
      console.log('- git stash (to save temporarily)');
    }
  } catch (e) {
    // Silent fail
  }

  process.exit(0);
}

// Read input
let input = '';
process.stdin.on('data', (chunk) => (input += chunk));
process.stdin.on('end', () => suggestBackup(input));
