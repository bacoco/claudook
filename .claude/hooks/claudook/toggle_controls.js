#!/usr/bin/env node

/**
 * Toggle Controls - JavaScript Version
 * Manages feature flags for Claudook
 */

const fs = require('fs');
const path = require('path');

function findProjectRoot(dir = process.cwd()) {
  while (dir !== '/') {
    if (fs.existsSync(path.join(dir, '.claude'))) {
      return dir;
    }
    dir = path.dirname(dir);
  }
  return null;
}

const root = findProjectRoot();
if (!root) {
  console.error('Could not find .claude directory');
  process.exit(1);
}

const claudeDir = path.join(root, '.claude');
const choicesFile = path.join(claudeDir, 'choices_enabled');
const testsFile = path.join(claudeDir, 'tests_enabled');
const parallelFile = path.join(claudeDir, 'parallel_enabled');

const command = process.argv[2];

function isEnabled(file) {
  return fs.existsSync(file);
}

function enable(file, feature) {
  fs.writeFileSync(file, '');
  console.log(`✅ ${feature} ENABLED`);
}

function disable(file, feature) {
  if (fs.existsSync(file)) {
    fs.unlinkSync(file);
  }
  console.log(`🔴 ${feature} DISABLED`);
}

function showStatus() {
  const choicesEnabled = isEnabled(choicesFile);
  const testsEnabled = isEnabled(testsFile);
  const parallelEnabled = isEnabled(parallelFile);

  console.log('🚀 CLAUDOOK STATUS');
  console.log('=====================\n');
  console.log('📊 Feature Status:');
  console.log(`  🎯 Multiple Choice System: ${choicesEnabled ? '🟢 ON' : '🔴 OFF'}`);
  console.log(`  🧪 Automatic Testing:      ${testsEnabled ? '🟢 ON' : '🔴 OFF'}`);
  console.log(`  🚀 Parallel Task Execution: ${parallelEnabled ? '🟢 ON' : '🔴 OFF'}`);
  console.log('\n💡 Claudook Commands:');
  console.log('  /claudook/help            - Show all available commands');
  console.log('  /claudook/status          - Show this status');
  console.log('  /claudook/choices-enable  - Turn on A/B/C option system');
  console.log('  /claudook/choices-disable - Turn off A/B/C option system');
  console.log('  /claudook/tests-enable    - Turn on mandatory testing');
  console.log('  /claudook/tests-disable   - Turn off mandatory testing');
  console.log('  /claudook/parallel-enable - Turn on parallel task execution');
  console.log('  /claudook/parallel-disable - Turn off parallel task execution');
  console.log('\n🎨 More Commands:');
  console.log('  /claudook/security-check  - Run security analysis');
  console.log('  /claudook/performance-check - Analyze performance');
  console.log('  /claudook/lint            - Code quality checks');
  console.log('  /claudook/config-show     - View configuration');
  console.log('  /claudook/update          - Check for updates');
  console.log('\n🎛️ Quick Toggle:');
  console.log('  node .claude/hooks/claudook/toggle_controls.js enable-choices');
  console.log('  node .claude/hooks/claudook/toggle_controls.js enable-tests');
  console.log('  node .claude/hooks/claudook/toggle_controls.js enable-parallel');
  console.log('  node .claude/hooks/claudook/toggle_controls.js disable-choices');
  console.log('  node .claude/hooks/claudook/toggle_controls.js disable-tests');
  console.log('  node .claude/hooks/claudook/toggle_controls.js disable-parallel');
  console.log('\n📚 Features Overview:\n');
  console.log('🎯 Multiple Choice System:');
  console.log('   When enabled, Claude automatically offers A/B/C options for complex');
  console.log('   questions, helping you choose the best approach before implementation.\n');
  console.log('🧪 Automatic Testing:');
  console.log('   When enabled, Claude is blocked after code changes until it creates');
  console.log('   comprehensive tests and ensures they pass. No exceptions.\n');
  console.log('🚀 Parallel Task Execution:');
  console.log('   When enabled, Claude automatically decomposes complex requests into');
  console.log('   subtasks, analyzes dependencies, and executes independent tasks in');
  console.log('   parallel using specialized agents.\n');
  console.log('🔍 Other Active Features:');
  console.log('   ✅ Security Guard (always active)');
  console.log('   ✅ Performance Optimizer (always active)');
  console.log('   ✅ Documentation Enforcer (always active)');
  console.log('   ✅ Git Backup Suggestions (always active)');
  console.log('   ✅ Usage Analytics (always active)');
  console.log('\n🎉 Your Claude CLI is enhanced with Claudook!');
}

switch (command) {
  case 'status':
    showStatus();
    break;
  case 'enable-choices':
    enable(choicesFile, 'Multiple choices system');
    console.log('   Claude will now offer A/B/C options for complex questions');
    break;
  case 'disable-choices':
    disable(choicesFile, 'Multiple choices system');
    console.log('   Claude will no longer offer A/B/C options');
    break;
  case 'enable-tests':
    enable(testsFile, 'Automatic testing');
    console.log('   Claude will be forced to create and run tests after code changes');
    break;
  case 'disable-tests':
    disable(testsFile, 'Automatic testing');
    console.log('   Claude will no longer be forced to create tests');
    break;
  case 'enable-parallel':
    enable(parallelFile, 'Parallel task execution');
    console.log('   Claude will decompose complex tasks and execute them in parallel');
    break;
  case 'disable-parallel':
    disable(parallelFile, 'Parallel task execution');
    console.log('   Claude will execute tasks sequentially');
    break;
  default:
    showStatus();
}
