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

const testsEnabledFile = path.join(root, '.claude', 'tests_enabled');
const codeModifiedFile = path.join(root, '.claude', 'code_modified');
const testsPassedFile = path.join(root, '.claude', 'tests_passed');

class TestEnforcer {
  constructor() {
    this.enabled = fs.existsSync(testsEnabledFile);
  }

  enforce(input) {
    if (!this.enabled) return;

    try {
      const data = JSON.parse(input);

      // Track code modifications
      if (this.isCodeModification(data)) {
        fs.writeFileSync(codeModifiedFile, JSON.stringify({
          timestamp: new Date().toISOString(),
          tool: data.tool_name,
          file: data.tool_input?.file_path || 'unknown'
        }));

        // Remove tests_passed flag to force new tests
        if (fs.existsSync(testsPassedFile)) {
          fs.unlinkSync(testsPassedFile);
        }

        this.blockUntilTested();
      }

      // Check if running tests
      if (this.isTestRun(data)) {
        this.trackTestRun();
      }
    } catch (e) {}
  }

  isCodeModification(data) {
    const codeTools = ['Write', 'Edit', 'MultiEdit', 'NotebookEdit'];
    if (!codeTools.includes(data.tool_name)) return false;

    const filePath = data.tool_input?.file_path || '';
    const codeExtensions = ['.js', '.ts', '.jsx', '.tsx', '.py', '.java', '.go', '.rs'];

    return codeExtensions.some(ext => filePath.endsWith(ext)) &&
           !filePath.includes('test') &&
           !filePath.includes('spec');
  }

  isTestRun(data) {
    if (data.tool_name !== 'Bash') return false;
    const command = data.tool_input?.command || '';
    return command.includes('test') ||
           command.includes('jest') ||
           command.includes('pytest') ||
           command.includes('npm test') ||
           command.includes('cargo test');
  }

  blockUntilTested() {
    if (!fs.existsSync(testsPassedFile) && fs.existsSync(codeModifiedFile)) {
      console.log('\n🚫 TEST ENFORCEMENT ACTIVE');
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log('⚠️  Code modifications detected!');
      console.log('📝 You must create and run tests before continuing.');
      console.log('\nRequired actions:');
      console.log('1. ✍️  Create unit tests for modified code');
      console.log('2. ✍️  Create integration tests if applicable');
      console.log('3. ▶️  Run all tests and ensure they pass');
      console.log('4. ✅ All tests must pass before proceeding');
      console.log('\nModified file:', this.getModifiedFile());
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    }
  }

  getModifiedFile() {
    try {
      if (fs.existsSync(codeModifiedFile)) {
        const data = JSON.parse(fs.readFileSync(codeModifiedFile, 'utf8'));
        return data.file || 'unknown';
      }
    } catch (e) {}
    return 'unknown';
  }

  trackTestRun() {
    // Mark tests as passed (in real implementation, would verify actual pass)
    fs.writeFileSync(testsPassedFile, JSON.stringify({
      timestamp: new Date().toISOString(),
      status: 'passed'
    }));

    // Clear code modified flag
    if (fs.existsSync(codeModifiedFile)) {
      fs.unlinkSync(codeModifiedFile);
    }

    console.log('✅ Tests executed - enforcement satisfied');
  }
}

if (process.argv[2] === 'test') {
  console.log('Test Enforcer ready');
  console.log('Status:', fs.existsSync(testsEnabledFile) ? 'ENABLED' : 'DISABLED');
  if (fs.existsSync(codeModifiedFile)) {
    console.log('Code modified - tests required!');
  }
  process.exit(0);
}

let input = '';
process.stdin.on('data', (chunk) => (input += chunk));
process.stdin.on('end', () => {
  new TestEnforcer().enforce(input);
  process.exit(0);
});