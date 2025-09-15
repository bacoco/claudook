#!/usr/bin/env node

/**
 * Security Guard Hook - JavaScript Version
 * Blocks dangerous operations before execution
 */

const fs = require('fs');
const path = require('path');

// Dangerous patterns to block
const DANGEROUS_PATTERNS = [
  { pattern: /rm\s+-rf\s+\/(?:\s|$)/, message: 'Attempting to delete root filesystem' },
  { pattern: /rm\s+-rf\s+~/, message: 'Attempting to delete home directory' },
  { pattern: /:\(\)\s*\{\s*:\|\s*:\s*&\s*\}\s*;/, message: 'Fork bomb detected' },
  { pattern: /dd\s+if=\/dev\/zero\s+of=\/dev\/[sh]da/, message: 'Attempting to overwrite disk' },
  { pattern: /mkfs\.\w+\s+\/dev\/[sh]da(?:\d+)?/, message: 'Attempting to format system disk' },
  { pattern: />\/dev\/[sh]da/, message: 'Attempting to write directly to disk' },
  { pattern: /chmod\s+777\s+\//, message: 'Making root filesystem world-writable' },
  { pattern: /curl.*\|\s*(?:bash|sh)/, message: 'Piping untrusted scripts to shell' },
  { pattern: /wget.*\|\s*(?:bash|sh)/, message: 'Piping untrusted scripts to shell' },
];

// Sensitive file patterns
const SENSITIVE_FILES = [
  /\/etc\/passwd/,
  /\/etc\/shadow/,
  /\.ssh\/id_[rd]sa/,
  /\.aws\/credentials/,
  /\.env$/,
  /private\.key/,
  /secret/i,
];

function checkSecurity(input) {
  try {
    const data = JSON.parse(input);

    if (data.tool_name === 'Bash' && data.tool_input?.command) {
      const command = data.tool_input.command;

      // Check dangerous patterns
      for (const { pattern, message } of DANGEROUS_PATTERNS) {
        if (pattern.test(command)) {
          console.error(`⛔ SECURITY BLOCK: ${message}`);
          console.error(`Dangerous command detected: ${command}`);
          console.error('\nSuggested safer alternatives:');
          console.error('- Use specific paths instead of /');
          console.error('- Create backups before deletion');
          console.error('- Use trash instead of rm for recovery');
          process.exit(1);
        }
      }
    }

    // Check file operations
    if (['Edit', 'Write', 'Read'].includes(data.tool_name) && data.tool_input?.file_path) {
      const filePath = data.tool_input.file_path;

      for (const pattern of SENSITIVE_FILES) {
        if (pattern.test(filePath)) {
          console.log(`⚠️ WARNING: Accessing sensitive file: ${filePath}`);
          console.log('Please ensure this operation is intentional');
          break;
        }
      }
    }
  } catch (e) {
    // Silent fail for non-JSON input
  }

  process.exit(0);
}

// Read input
let input = '';
process.stdin.on('data', (chunk) => (input += chunk));
process.stdin.on('end', () => checkSecurity(input));
