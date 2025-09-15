#!/usr/bin/env node
import { spawn } from 'child_process';
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

class HookRunner {
  async runHooks(phase, data) {
    const hooksDir = path.join(root, '.claude', 'hooks', 'claudook');
    const hooks = fs.readdirSync(hooksDir).filter(f => f.endsWith('.js'));
    
    for (const hook of hooks) {
      const hookPath = path.join(hooksDir, hook);
      const child = spawn('node', [hookPath], { stdio: ['pipe', 'inherit', 'inherit'] });
      child.stdin.write(JSON.stringify(data));
      child.stdin.end();
      await new Promise(resolve => child.on('exit', resolve));
    }
  }
}

if (process.argv[2] === 'test') {
  console.log('Hook Runner ready');
  process.exit(0);
}

let input = '';
process.stdin.on('data', (chunk) => (input += chunk));
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);
    new HookRunner().runHooks('before', data);
  } catch (e) {}
  process.exit(0);
});
