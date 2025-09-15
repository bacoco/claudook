#!/usr/bin/env node

/**
 * Task Analyzer - JavaScript Version
 * Analyzes task complexity and characteristics
 */

import fs from 'fs';
import path from 'path';

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
if (!root) process.exit(0);

class TaskAnalyzer {
  analyzeComplexity(text) {
    const indicators = {
      simple: ['fix', 'update', 'change', 'modify', 'rename'],
      medium: ['add', 'create', 'implement', 'integrate'],
      complex: ['refactor', 'redesign', 'architect', 'migrate', 'optimize entire']
    };

    const textLower = text.toLowerCase();
    let complexity = 'simple';
    let score = 1;

    if (indicators.complex.some(i => textLower.includes(i))) {
      complexity = 'complex';
      score = 3;
    } else if (indicators.medium.some(i => textLower.includes(i))) {
      complexity = 'medium';
      score = 2;
    }

    // Additional factors
    if (textLower.includes('test') && textLower.includes('document')) score++;
    if (textLower.includes('performance') || textLower.includes('security')) score++;
    if (textLower.split(' and ').length > 2) score++;

    return { complexity, score: Math.min(score, 5) };
  }

  analyzeType(text) {
    const types = {
      feature: ['feature', 'implement', 'add', 'create new'],
      bugfix: ['fix', 'bug', 'issue', 'error', 'problem'],
      refactor: ['refactor', 'clean', 'reorganize', 'restructure'],
      test: ['test', 'unit test', 'integration', 'e2e'],
      docs: ['document', 'docs', 'readme', 'comment'],
      performance: ['optimize', 'performance', 'speed', 'faster'],
      security: ['security', 'vulnerability', 'auth', 'permission']
    };

    const textLower = text.toLowerCase();

    for (const [type, keywords] of Object.entries(types)) {
      if (keywords.some(k => textLower.includes(k))) {
        return type;
      }
    }

    return 'feature'; // default
  }

  estimateTime(complexity, text) {
    const baseTime = {
      simple: 30,
      medium: 120,
      complex: 480
    };

    let minutes = baseTime[complexity.complexity] || 60;

    // Adjust based on text length and content
    if (text.length > 200) minutes *= 1.5;
    if (text.includes('test')) minutes += 30;
    if (text.includes('document')) minutes += 20;

    return {
      minutes: Math.round(minutes),
      formatted: `${Math.round(minutes / 60)}h ${minutes % 60}m`
    };
  }

  analyzeDependencies(text) {
    const deps = [];
    const textLower = text.toLowerCase();

    // Common dependency patterns
    if (textLower.includes('after') || textLower.includes('then')) {
      deps.push('sequential');
    }
    if (textLower.includes('test') && !textLower.startsWith('test')) {
      deps.push('requires_implementation');
    }
    if (textLower.includes('deploy')) {
      deps.push('requires_testing');
    }
    if (textLower.includes('document') && !textLower.startsWith('document')) {
      deps.push('requires_completion');
    }

    return deps;
  }

  analyze(text) {
    const complexity = this.analyzeComplexity(text);
    const type = this.analyzeType(text);
    const time = this.estimateTime(complexity, text);
    const dependencies = this.analyzeDependencies(text);

    return {
      text,
      complexity,
      type,
      estimatedTime: time,
      dependencies,
      priority: complexity.score >= 3 ? 'high' : complexity.score >= 2 ? 'medium' : 'low',
      requiresReview: complexity.score >= 3 || type === 'security',
      canParallelize: dependencies.length === 0
    };
  }

  process(input) {
    try {
      const data = JSON.parse(input);

      if (data.type === 'analyze_task' && data.content) {
        const analysis = this.analyze(data.content);
        console.log(JSON.stringify(analysis, null, 2));
      }
    } catch (e) {
      // Silent fail
    }
  }
}

// Main execution
if (process.argv[2] === 'test') {
  const analyzer = new TaskAnalyzer();
  const result = analyzer.analyze('Refactor the authentication system, add tests, and document the API');
  console.log('Analysis:', result);
  process.exit(0);
}

// Read input from stdin
let input = '';
process.stdin.on('data', (chunk) => (input += chunk));
process.stdin.on('end', () => {
  const analyzer = new TaskAnalyzer();
  analyzer.process(input);
  process.exit(0);
});