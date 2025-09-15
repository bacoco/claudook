#!/usr/bin/env node

/**
 * Universal Hook Runner for Claudook
 *
 * This Node.js runner solves the Python path issues by:
 * 1. Automatically finding the project root (.claude directory)
 * 2. Running hooks from the correct directory
 * 3. Working from any subdirectory without path issues
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Find the .claude directory by traversing up
function findProjectRoot(startDir = process.cwd()) {
  let currentDir = startDir;

  while (currentDir !== '/') {
    const claudeDir = path.join(currentDir, '.claude');
    if (fs.existsSync(claudeDir)) {
      return currentDir;
    }
    currentDir = path.dirname(currentDir);
  }

  throw new Error('Could not find .claude directory in any parent directory');
}

// Main execution
async function main() {
  try {
    // Get the script to run from arguments
    const args = process.argv.slice(2);
    if (args.length === 0) {
      console.error('Usage: node hook_runner.js <script.py> [args...]');
      process.exit(1);
    }

    const scriptName = args[0];
    const scriptArgs = args.slice(1);

    // Find project root
    const projectRoot = findProjectRoot();
    const hooksDir = path.join(projectRoot, '.claude', 'hooks', 'claudook');
    const scriptPath = path.join(hooksDir, scriptName);

    // Check if script exists
    if (!fs.existsSync(scriptPath)) {
      // Silently exit for missing hooks (non-blocking)
      process.exit(0);
    }

    // Change to project root for consistent execution
    process.chdir(projectRoot);

    // Run the Python script
    const python = spawn('python3', [scriptPath, ...scriptArgs], {
      cwd: projectRoot,
      stdio: 'inherit',
      env: {
        ...process.env,
        PROJECT_ROOT: projectRoot,
        HOOKS_DIR: hooksDir,
      },
    });

    python.on('error', (err) => {
      // Silently handle errors (non-blocking)
      process.exit(0);
    });

    python.on('exit', (code) => {
      process.exit(code || 0);
    });
  } catch (error) {
    // Silently exit on any error (non-blocking)
    process.exit(0);
  }
}

// Handle stdin if needed
if (!process.stdin.isTTY) {
  let inputData = '';
  process.stdin.on('data', (chunk) => {
    inputData += chunk;
  });
  process.stdin.on('end', () => {
    process.env.HOOK_INPUT = inputData;
    main();
  });
} else {
  main();
}
