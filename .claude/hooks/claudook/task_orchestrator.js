#!/usr/bin/env node

/**
 * Task Orchestrator - JavaScript Version
 * Decomposes complex tasks and manages parallel execution
 * Creates GitHub-compatible task lists in .claude/tasks/
 */

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';

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

const TASKS_DIR = path.join(root, '.claude', 'tasks');
const PARALLEL_ENABLED = path.join(root, '.claude', 'parallel_enabled');

class TaskOrchestrator {
  constructor() {
    this.sessionId = new Date().toISOString().replace(/[:.]/g, '-');
    this.tasks = [];
    this.dependencies = {};
    this.parallelGroups = [];
  }

  analyzeComplexity(prompt) {
    const promptLower = prompt.toLowerCase();

    const complexKeywords = ['implement', 'create', 'build', 'refactor', 'integrate', 'deploy'];
    const mediumKeywords = ['update', 'modify', 'fix', 'add', 'change'];

    if (complexKeywords.some(k => promptLower.includes(k))) return 3;
    if (mediumKeywords.some(k => promptLower.includes(k))) return 2;
    return 1;
  }

  decomposeTasks(prompt) {
    const tasks = [];
    const complexity = this.analyzeComplexity(prompt);

    if (complexity >= 2) {
      // Extract potential tasks from prompt
      const actions = prompt.match(/(?:implement|create|build|update|fix|add|test|document)\s+[\w\s]+/gi) || [];

      actions.forEach(action => {
        tasks.push({
          id: crypto.randomBytes(8).toString('hex'),
          title: action.trim(),
          description: `Task: ${action}`,
          status: 'pending',
          priority: 'medium',
          dependencies: [],
          assignee: null,
          created: new Date().toISOString()
        });
      });
    }

    // If no tasks found, create a single task
    if (tasks.length === 0) {
      tasks.push({
        id: crypto.randomBytes(8).toString('hex'),
        title: prompt.substring(0, 50),
        description: prompt,
        status: 'pending',
        priority: 'medium',
        dependencies: [],
        assignee: null,
        created: new Date().toISOString()
      });
    }

    this.tasks = tasks;
    return tasks;
  }

  analyzeDependencies() {
    // Simple dependency analysis based on keywords
    this.tasks.forEach((task, index) => {
      const taskLower = task.title.toLowerCase();

      // Testing depends on implementation
      if (taskLower.includes('test') && index > 0) {
        task.dependencies = [this.tasks[0].id];
      }

      // Documentation depends on everything
      if (taskLower.includes('document') && index > 0) {
        task.dependencies = this.tasks.slice(0, index).map(t => t.id);
      }

      // Deployment depends on testing
      if (taskLower.includes('deploy')) {
        const testTask = this.tasks.find(t => t.title.toLowerCase().includes('test'));
        if (testTask) task.dependencies = [testTask.id];
      }
    });

    return this.dependencies;
  }

  identifyParallelGroups() {
    const groups = [];
    const processed = new Set();

    // Group tasks with no dependencies
    const independent = this.tasks.filter(t => t.dependencies.length === 0);
    if (independent.length > 0) {
      groups.push({
        groupId: 0,
        tasks: independent.map(t => t.id),
        canRunParallel: true
      });
      independent.forEach(t => processed.add(t.id));
    }

    // Group remaining tasks by dependencies
    let groupId = 1;
    while (processed.size < this.tasks.length) {
      const group = this.tasks.filter(t =>
        !processed.has(t.id) &&
        t.dependencies.every(d => processed.has(d))
      );

      if (group.length > 0) {
        groups.push({
          groupId: groupId++,
          tasks: group.map(t => t.id),
          canRunParallel: true
        });
        group.forEach(t => processed.add(t.id));
      } else {
        break; // Prevent infinite loop
      }
    }

    this.parallelGroups = groups;
    return groups;
  }

  generateMasterTasks() {
    const sessionDir = path.join(TASKS_DIR, `session_${this.sessionId}`);
    fs.mkdirSync(sessionDir, { recursive: true });

    const masterFile = path.join(sessionDir, 'MASTER_TASKS.md');

    let content = '# Master Task List\n\n';
    content += `**Session:** ${this.sessionId}\n`;
    content += `**Created:** ${new Date().toISOString()}\n`;
    content += `**Total Tasks:** ${this.tasks.length}\n\n`;

    // Group by priority
    const priorities = ['high', 'medium', 'low'];

    priorities.forEach(priority => {
      const priorityTasks = this.tasks.filter(t => t.priority === priority);
      if (priorityTasks.length > 0) {
        content += `## ${priority.charAt(0).toUpperCase() + priority.slice(1)} Priority\n\n`;

        priorityTasks.forEach(task => {
          const checkbox = task.status === 'completed' ? '[x]' : '[ ]';
          const assignee = task.assignee ? ` @${task.assignee}` : '';
          const deps = task.dependencies.length > 0 ? ` (depends on: ${task.dependencies.join(', ')})` : '';

          content += `- ${checkbox} **${task.title}**${assignee}${deps}\n`;
          content += `  - ID: ${task.id}\n`;
          content += `  - ${task.description}\n\n`;
        });
      }
    });

    // Add parallel execution plan
    if (this.parallelGroups.length > 0) {
      content += '## Parallel Execution Plan\n\n';
      this.parallelGroups.forEach(group => {
        content += `### Stage ${group.groupId + 1}\n`;
        content += 'Tasks that can run in parallel:\n';
        group.tasks.forEach(taskId => {
          const task = this.tasks.find(t => t.id === taskId);
          content += `- ${task.title}\n`;
        });
        content += '\n';
      });
    }

    fs.writeFileSync(masterFile, content);

    // Create symlink in main tasks directory
    const mainMaster = path.join(TASKS_DIR, 'MASTER_TASKS.md');
    if (fs.existsSync(mainMaster)) {
      fs.unlinkSync(mainMaster);
    }
    fs.symlinkSync(masterFile, mainMaster);

    return masterFile;
  }

  generateExecutionDashboard() {
    const sessionDir = path.join(TASKS_DIR, `session_${this.sessionId}`);
    const dashboardFile = path.join(sessionDir, 'EXECUTION_DASHBOARD.md');

    let content = '# Execution Dashboard\n\n';
    content += `**Session:** ${this.sessionId}\n`;
    content += `**Last Updated:** ${new Date().toISOString()}\n\n`;

    // Status overview
    const pending = this.tasks.filter(t => t.status === 'pending').length;
    const inProgress = this.tasks.filter(t => t.status === 'in_progress').length;
    const completed = this.tasks.filter(t => t.status === 'completed').length;

    content += '## Status Overview\n\n';
    content += '```\n';
    content += `📋 Pending:     ${pending}\n`;
    content += `🔄 In Progress: ${inProgress}\n`;
    content += `✅ Completed:   ${completed}\n`;
    content += '```\n\n';

    // Progress bar
    const total = this.tasks.length;
    const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
    const barLength = 20;
    const filled = Math.round((progress / 100) * barLength);
    const empty = barLength - filled;

    content += '## Progress\n\n';
    content += `[${'█'.repeat(filled)}${'░'.repeat(empty)}] ${progress}%\n\n`;

    // Current execution stage
    if (this.parallelGroups.length > 0) {
      const currentStage = this.parallelGroups.find(g =>
        g.tasks.some(id => {
          const task = this.tasks.find(t => t.id === id);
          return task.status === 'in_progress';
        })
      );

      if (currentStage) {
        content += `## Current Stage: ${currentStage.groupId + 1}\n\n`;
        content += 'Running in parallel:\n';
        currentStage.tasks.forEach(taskId => {
          const task = this.tasks.find(t => t.id === taskId);
          const icon = task.status === 'completed' ? '✅' :
                       task.status === 'in_progress' ? '🔄' : '⏳';
          content += `- ${icon} ${task.title}\n`;
        });
        content += '\n';
      }
    }

    // Task details
    content += '## Task Details\n\n';
    this.tasks.forEach(task => {
      const icon = task.status === 'completed' ? '✅' :
                   task.status === 'in_progress' ? '🔄' : '📋';
      content += `### ${icon} ${task.title}\n`;
      content += `- **ID:** ${task.id}\n`;
      content += `- **Status:** ${task.status}\n`;
      content += `- **Priority:** ${task.priority}\n`;
      if (task.dependencies.length > 0) {
        content += `- **Dependencies:** ${task.dependencies.join(', ')}\n`;
      }
      content += '\n';
    });

    fs.writeFileSync(dashboardFile, content);

    // Create symlink in main tasks directory
    const mainDashboard = path.join(TASKS_DIR, 'EXECUTION_DASHBOARD.md');
    if (fs.existsSync(mainDashboard)) {
      fs.unlinkSync(mainDashboard);
    }
    fs.symlinkSync(dashboardFile, mainDashboard);

    return dashboardFile;
  }

  exportToGitHub() {
    const sessionDir = path.join(TASKS_DIR, `session_${this.sessionId}`);
    const githubFile = path.join(sessionDir, 'GITHUB_TASKS.md');

    let content = '# GitHub Task List\n\n';
    content += 'Copy this to your GitHub issue or PR:\n\n';
    content += '---\n\n';

    this.tasks.forEach(task => {
      const checkbox = task.status === 'completed' ? '- [x]' : '- [ ]';
      const labels = [];
      if (task.priority === 'high') labels.push('priority:high');
      if (task.title.toLowerCase().includes('bug')) labels.push('bug');
      if (task.title.toLowerCase().includes('feature')) labels.push('enhancement');

      const labelStr = labels.length > 0 ? ` [${labels.join(', ')}]` : '';
      content += `${checkbox} ${task.title}${labelStr}\n`;
    });

    fs.writeFileSync(githubFile, content);
    return githubFile;
  }

  process(input) {
    try {
      // Always check if parallel execution is enabled
      const parallelEnabled = fs.existsSync(PARALLEL_ENABLED);

      let taskContent = '';

      try {
        const data = JSON.parse(input);

        // Handle different input types
        if (data.type === 'user_prompt') {
          taskContent = data.content || '';
        } else if (data.tool === 'TodoWrite' && data.params) {
          // Handle TodoWrite events - extract todos
          const todos = data.params.todos || [];
          if (todos.length > 0) {
            taskContent = todos.map(t => t.content || t.title || '').join(', ');

            // Convert todos to tasks
            this.tasks = todos.map(todo => ({
              id: crypto.randomBytes(8).toString('hex'),
              title: todo.content || todo.title || 'Task',
              description: todo.activeForm || todo.content || '',
              status: todo.status || 'pending',
              priority: 'medium',
              dependencies: [],
              assignee: null,
              created: new Date().toISOString()
            }));
          }
        } else if (typeof data === 'string') {
          taskContent = data;
        }
      } catch (parseError) {
        // If not JSON, treat as plain text
        taskContent = input.toString().trim();
      }

      // If we have tasks from TodoWrite, generate files
      if (this.tasks.length > 0 && parallelEnabled) {
        // Analyze dependencies
        this.analyzeDependencies();

        // Identify parallel groups
        this.identifyParallelGroups();

        // Generate files
        this.generateMasterTasks();
        this.generateExecutionDashboard();
        this.exportToGitHub();

        console.log(`📋 Task Orchestrator: Created ${this.tasks.length} tasks`);
        console.log(`📁 Tasks saved to: .claude/tasks/session_${this.sessionId}/`);
        console.log(`🚀 Parallel execution groups: ${this.parallelGroups.length}`);
      } else if (taskContent && parallelEnabled) {
        // Decompose tasks from content
        this.decomposeTasks(taskContent);

        if (this.tasks.length > 1) {
          // Analyze dependencies
          this.analyzeDependencies();

          // Identify parallel groups
          this.identifyParallelGroups();

          // Generate files
          this.generateMasterTasks();
          this.generateExecutionDashboard();
          this.exportToGitHub();

          console.log(`📋 Task Orchestrator: Created ${this.tasks.length} tasks`);
          console.log(`📁 Tasks saved to: .claude/tasks/session_${this.sessionId}/`);
          console.log(`🚀 Parallel execution groups: ${this.parallelGroups.length}`);
        }
      }
    } catch (e) {
      // Log error for debugging but don't break
      if (process.env.DEBUG) {
        console.error('Task Orchestrator Error:', e);
      }
    }
  }
}

// Main execution
if (process.argv[2] === 'test') {
  const orchestrator = new TaskOrchestrator();
  orchestrator.decomposeTasks('Implement user authentication, create tests, and document the API');
  orchestrator.analyzeDependencies();
  orchestrator.identifyParallelGroups();
  console.log('Tasks:', orchestrator.tasks);
  console.log('Parallel Groups:', orchestrator.parallelGroups);
  process.exit(0);
}

// Read input from stdin
let input = '';
process.stdin.on('data', (chunk) => (input += chunk));
process.stdin.on('end', () => {
  const orchestrator = new TaskOrchestrator();
  orchestrator.process(input);
  process.exit(0);
});