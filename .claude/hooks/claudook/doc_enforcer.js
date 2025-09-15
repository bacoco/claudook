#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

function findProjectRoot(dir = process.cwd()) {
  while (dir !== '/') {
    if (fs.existsSync(path.join(dir, '.claude'))) return dir;
    dir = path.dirname(dir);
  }
  return null;
}

const root = findProjectRoot();
if (!root) process.exit(0);

class DocEnforcer {
  check(input) {
    try {
      const data = JSON.parse(input);
      if ((data.tool_name === 'Write' || data.tool_name === 'Edit') && data.tool_input?.file_path?.endsWith('.js')) {
        console.log('📝 Remember to add JSDoc comments for public functions');
      }
    } catch (e) {}
  }
}

if (process.argv[2] === 'test') {
  console.log('Doc Enforcer ready');
  process.exit(0);
}

let input = '';
process.stdin.on('data', (chunk) => (input += chunk));
process.stdin.on('end', () => {
  new DocEnforcer().check(input);
  process.exit(0);
});
