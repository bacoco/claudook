#!/usr/bin/env node

/**
 * Dependency Analyzer - JavaScript Version
 * Analyzes dependencies between tasks for parallel execution
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

class DependencyAnalyzer {
  analyzeDependencies(tasks) {
    const dependencies = {};
    const graph = {};

    tasks.forEach(task => {
      graph[task.id] = [];
      const taskLower = task.title.toLowerCase();

      // Analyze dependencies based on keywords
      tasks.forEach(otherTask => {
        if (task.id === otherTask.id) return;

        const otherLower = otherTask.title.toLowerCase();

        // Tests depend on implementation
        if (taskLower.includes('test') && otherLower.includes('implement')) {
          graph[task.id].push(otherTask.id);
        }

        // Documentation depends on implementation
        if (taskLower.includes('document') && 
            (otherLower.includes('implement') || otherLower.includes('create'))) {
          graph[task.id].push(otherTask.id);
        }

        // Deployment depends on testing
        if (taskLower.includes('deploy') && otherLower.includes('test')) {
          graph[task.id].push(otherTask.id);
        }

        // Refactoring should happen before new features
        if (taskLower.includes('feature') && otherLower.includes('refactor')) {
          graph[task.id].push(otherTask.id);
        }
      });

      dependencies[task.id] = graph[task.id];
    });

    return { dependencies, graph };
  }

  findParallelGroups(tasks, dependencies) {
    const groups = [];
    const completed = new Set();
    let groupId = 0;

    while (completed.size < tasks.length) {
      const group = tasks.filter(task =>
        !completed.has(task.id) &&
        dependencies[task.id].every(dep => completed.has(dep))
      );

      if (group.length === 0 && completed.size < tasks.length) {
        // Circular dependency detected
        console.warn('⚠️ Circular dependency detected');
        break;
      }

      if (group.length > 0) {
        groups.push({
          id: groupId++,
          tasks: group.map(t => t.id),
          canParallelize: true
        });
        group.forEach(t => completed.add(t.id));
      }
    }

    return groups;
  }

  process(input) {
    try {
      const data = JSON.parse(input);

      if (data.type === 'analyze_dependencies' && data.tasks) {
        const { dependencies, graph } = this.analyzeDependencies(data.tasks);
        const groups = this.findParallelGroups(data.tasks, dependencies);

        console.log(JSON.stringify({ dependencies, graph, groups }, null, 2));
      }
    } catch (e) {
      // Silent fail
    }
  }
}

// Main execution
if (process.argv[2] === 'test') {
  const analyzer = new DependencyAnalyzer();
  const tasks = [
    { id: '1', title: 'Implement feature' },
    { id: '2', title: 'Test feature' },
    { id: '3', title: 'Document feature' }
  ];
  const result = analyzer.analyzeDependencies(tasks);
  const groups = analyzer.findParallelGroups(tasks, result.dependencies);
  console.log('Dependencies:', result);
  console.log('Parallel groups:', groups);
  process.exit(0);
}

// Read input from stdin
let input = '';
process.stdin.on('data', (chunk) => (input += chunk));
process.stdin.on('end', () => {
  const analyzer = new DependencyAnalyzer();
  analyzer.process(input);
  process.exit(0);
});
