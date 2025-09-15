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

const CONTEXT_FILE = path.join(root, '.claude', 'context.json');

class SmartContext {
  saveContext(data) {
    const context = fs.existsSync(CONTEXT_FILE) ? JSON.parse(fs.readFileSync(CONTEXT_FILE, 'utf8')) : {};
    context.lastUpdate = new Date().toISOString();
    context.data = { ...context.data, ...data };
    fs.writeFileSync(CONTEXT_FILE, JSON.stringify(context, null, 2));
  }
}

if (process.argv[2] === 'test') {
  console.log('Smart Context ready');
  process.exit(0);
}

let input = '';
process.stdin.on('data', (chunk) => (input += chunk));
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);
    new SmartContext().saveContext({ tool: data.tool_name });
  } catch (e) {}
  process.exit(0);
});
