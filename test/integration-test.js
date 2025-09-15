#!/usr/bin/env node
import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.join(__dirname, '..');

console.log('🧪 Integration Test: Simulating real Claude usage\n');

// Test scenarios
const scenarios = [
  {
    name: 'Security Block Test',
    command: 'echo \'{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}\' | node .claude/hooks/claudook/security_guard.js',
    shouldContain: 'SECURITY BLOCK',
    description: 'Dangerous command should be blocked'
  },
  {
    name: 'Git Backup Suggestion',
    command: 'echo \'{"tool_name":"Write","tool_input":{"file_path":"app.js","content":"console.log()"}}\' | node .claude/hooks/claudook/git_backup.js',
    shouldContain: 'changes',
    description: 'Should suggest git commit after file changes'
  },
  {
    name: 'Performance Optimization',
    command: 'echo \'{"tool_name":"Write","tool_input":{"content":"for(let i=0;i<1000;i++){}"}}\' | node .claude/hooks/claudook/perf_optimizer.js',
    shouldContain: 'Consider',
    description: 'Should suggest performance improvements for loops'
  },
  {
    name: 'Documentation Enforcement',
    command: 'echo \'{"tool_name":"Write","tool_input":{"file_path":"utils.js"}}\' | node .claude/hooks/claudook/doc_enforcer.js',
    shouldContain: 'JSDoc',
    description: 'Should remind about JSDoc for JS files'
  },
  {
    name: 'Task Orchestration',
    command: 'echo \'{"tool_name":"TodoWrite","tool_input":{"prompt":"Build REST API"}}\' | node .claude/hooks/claudook/task_orchestrator.js',
    shouldContain: 'Task',
    description: 'Should decompose complex tasks'
  },
  {
    name: 'Multiple Choice System',
    command: 'echo \'{"tool_name":"WebSearch","tool_input":{"query":"which approach should I use"}}\' | node .claude/hooks/claudook/multiple_choice.js',
    shouldContain: 'CHOICE',
    description: 'Should present multiple choice options'
  },
  {
    name: 'Agent Spawning',
    command: 'echo \'{"tool_name":"Task","tool_input":{"tasks":["code","test"]}}\' | node .claude/hooks/claudook/agent_spawner.js',
    shouldContain: 'Spawned',
    description: 'Should spawn specialized agents'
  }
];

let passed = 0;
let failed = 0;

// Run each scenario
scenarios.forEach(scenario => {
  try {
    process.chdir(rootDir);
    const output = execSync(scenario.command, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] });

    if (output.includes(scenario.shouldContain)) {
      console.log(`✅ ${scenario.name}: PASSED`);
      console.log(`   ${scenario.description}`);
      passed++;
    } else {
      console.log(`❌ ${scenario.name}: FAILED`);
      console.log(`   Expected to contain: "${scenario.shouldContain}"`);
      console.log(`   Got: ${output.substring(0, 100)}...`);
      failed++;
    }
  } catch (error) {
    // Some hooks exit with non-zero for blocking
    if (scenario.name === 'Security Block Test' && error.stdout && error.stdout.includes('SECURITY BLOCK')) {
      console.log(`✅ ${scenario.name}: PASSED`);
      console.log(`   ${scenario.description}`);
      passed++;
    } else {
      console.log(`❌ ${scenario.name}: ERROR`);
      console.log(`   ${error.message}`);
      failed++;
    }
  }
  console.log();
});

// Test hook configuration
console.log('📋 Checking hook configuration...\n');

const settingsPath = path.join(rootDir, '.claude', 'settings.json');
const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));

// Check if PreToolUse is configured
if (settings.hooks && settings.hooks.PreToolUse) {
  console.log('✅ PreToolUse hooks configured');

  // Count hooks
  const totalHooks = settings.hooks.PreToolUse.reduce((count, matcher) => {
    return count + (matcher.hooks ? matcher.hooks.length : 0);
  }, 0);

  console.log(`✅ Total hooks configured: ${totalHooks}`);

  // Check for CLAUDE_PROJECT_DIR
  const hasProjectDir = JSON.stringify(settings).includes('${CLAUDE_PROJECT_DIR}');
  if (hasProjectDir) {
    console.log('✅ Using ${CLAUDE_PROJECT_DIR} for local execution');
  } else {
    console.log('⚠️  Not using ${CLAUDE_PROJECT_DIR} - hooks might not work locally');
  }
} else {
  console.log('❌ PreToolUse hooks not configured');
  failed++;
}

// Summary
console.log('\n' + '='.repeat(50));
console.log('📊 Integration Test Results:');
console.log(`   Scenarios Passed: ${passed}/${scenarios.length}`);
console.log(`   Configuration: ${settings.hooks?.PreToolUse ? 'Valid' : 'Invalid'}`);

const successRate = Math.round((passed / scenarios.length) * 100);
if (successRate === 100) {
  console.log('\n🎉 All integration tests passed!');
  process.exit(0);
} else {
  console.log(`\n⚠️  ${successRate}% tests passed`);
  process.exit(1);
}