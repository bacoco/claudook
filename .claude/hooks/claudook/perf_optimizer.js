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

class PerfOptimizer {
  analyze(input) {
    try {
      const data = JSON.parse(input);
      if (data.tool_name === 'Write' && data.tool_input?.content?.includes('for')) {
        console.log('⚡ Consider using Array methods like map/filter for better performance');
      }
    } catch (e) {}
  }
}

if (process.argv[2] === 'test') {
  console.log('Perf Optimizer ready');
  process.exit(0);
}

let input = '';
process.stdin.on('data', (chunk) => (input += chunk));
process.stdin.on('end', () => {
  new PerfOptimizer().analyze(input);
  process.exit(0);
});
