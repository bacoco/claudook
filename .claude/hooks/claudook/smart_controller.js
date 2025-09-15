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

class SmartController {
  autoManage(input) {
    try {
      const data = JSON.parse(input);
      console.log('Smart Controller: Monitoring', data.tool_name || 'activity');
    } catch (e) {}
  }
}

if (process.argv[2] === 'test') {
  console.log('Smart Controller ready');
  process.exit(0);
}

let input = '';
process.stdin.on('data', (chunk) => (input += chunk));
process.stdin.on('end', () => {
  new SmartController().autoManage(input);
  process.exit(0);
});
