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

const choicesEnabledFile = path.join(root, '.claude', 'choices_enabled');

class MultipleChoice {
  constructor() {
    this.enabled = fs.existsSync(choicesEnabledFile);
  }

  presentChoices(input) {
    if (!this.enabled) return;

    try {
      const data = JSON.parse(input);

      // Detect complex decisions in prompts
      if (data.tool_name === 'WebSearch' || data.tool_name === 'WebFetch') {
        const query = data.tool_input?.query || data.tool_input?.prompt || '';
        if (this.isComplexDecision(query)) {
          this.generateOptions(query);
        }
      }

      // Detect architecture decisions
      if (data.tool_name === 'Write' || data.tool_name === 'Edit') {
        const content = data.tool_input?.content || data.tool_input?.new_string || '';
        if (this.isArchitectureDecision(content)) {
          this.suggestArchitectureOptions();
        }
      }
    } catch (e) {}
  }

  isComplexDecision(text) {
    const complexKeywords = [
      'how should', 'what approach', 'which method', 'best way',
      'options for', 'alternatives', 'choose between', 'decide',
      'recommend', 'suggestion', 'preference'
    ];
    const lower = text.toLowerCase();
    return complexKeywords.some(keyword => lower.includes(keyword));
  }

  isArchitectureDecision(content) {
    const archKeywords = [
      'authentication', 'database', 'api', 'architecture',
      'framework', 'library', 'pattern', 'design', 'structure'
    ];
    const lower = content.toLowerCase();
    return archKeywords.some(keyword => lower.includes(keyword));
  }

  generateOptions(query) {
    console.log('\n🎯 MULTIPLE CHOICE SYSTEM ACTIVATED');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('Complex decision detected. Consider presenting options:');
    console.log('\n📋 Suggested Format:');
    console.log('**Option A: [Approach Name]**');
    console.log('- Pros: [advantages]');
    console.log('- Cons: [disadvantages]');
    console.log('- Time: [estimate]');
    console.log('\n**Option B: [Alternative Approach]**');
    console.log('- Pros: [advantages]');
    console.log('- Cons: [disadvantages]');
    console.log('- Time: [estimate]');
    console.log('\n**Option C: [Another Alternative]**');
    console.log('- Pros: [advantages]');
    console.log('- Cons: [disadvantages]');
    console.log('- Time: [estimate]');
    console.log('\nWhich would you prefer? (A/B/C)');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  }

  suggestArchitectureOptions() {
    console.log('\n🏗️ ARCHITECTURE DECISION POINT');
    console.log('Consider offering multiple implementation approaches');
  }
}

if (process.argv[2] === 'test') {
  console.log('Multiple Choice System ready');
  console.log('Status:', fs.existsSync(choicesEnabledFile) ? 'ENABLED' : 'DISABLED');
  process.exit(0);
}

let input = '';
process.stdin.on('data', (chunk) => (input += chunk));
process.stdin.on('end', () => {
  new MultipleChoice().presentChoices(input);
  process.exit(0);
});