#!/usr/bin/env node

/**
 * Agent Spawner - JavaScript Version
 * Spawns specialized agents for different task types
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

const AGENTS_DIR = path.join(root, '.claude', 'agents');

// Agent types and their specializations
const AGENT_TYPES = {
  coder: {
    name: 'Coder Agent',
    skills: ['implement', 'code', 'develop', 'program', 'refactor'],
    prompt: 'You are a specialized coding agent. Focus on clean, efficient code implementation.'
  },
  researcher: {
    name: 'Researcher Agent',
    skills: ['research', 'analyze', 'investigate', 'explore', 'study'],
    prompt: 'You are a research specialist. Gather information and provide insights.'
  },
  tester: {
    name: 'Tester Agent',
    skills: ['test', 'verify', 'validate', 'check', 'qa'],
    prompt: 'You are a testing specialist. Create comprehensive tests and ensure quality.'
  },
  documenter: {
    name: 'Documenter Agent',
    skills: ['document', 'explain', 'describe', 'write docs'],
    prompt: 'You are a documentation specialist. Create clear, comprehensive documentation.'
  },
  reviewer: {
    name: 'Reviewer Agent',
    skills: ['review', 'audit', 'inspect', 'evaluate'],
    prompt: 'You are a code review specialist. Identify issues and suggest improvements.'
  },
  optimizer: {
    name: 'Optimizer Agent',
    skills: ['optimize', 'improve', 'enhance', 'performance'],
    prompt: 'You are a performance optimization specialist. Improve efficiency and speed.'
  },
  architect: {
    name: 'Architect Agent',
    skills: ['design', 'architect', 'structure', 'plan'],
    prompt: 'You are a software architect. Design robust, scalable system architectures.'
  },
  debugger: {
    name: 'Debugger Agent',
    skills: ['debug', 'fix', 'troubleshoot', 'solve'],
    prompt: 'You are a debugging specialist. Find and fix bugs efficiently.'
  }
};

class AgentSpawner {
  constructor() {
    this.agents = [];
    this.sessionId = new Date().toISOString().replace(/[:.]/g, '-');
  }

  identifyAgentType(task) {
    const taskLower = task.toLowerCase();

    for (const [type, config] of Object.entries(AGENT_TYPES)) {
      if (config.skills.some(skill => taskLower.includes(skill))) {
        return type;
      }
    }

    return 'coder'; // Default to coder
  }

  spawnAgent(taskId, taskTitle, taskDescription, agentType = null) {
    // Auto-detect agent type if not specified
    if (!agentType) {
      agentType = this.identifyAgentType(taskTitle + ' ' + taskDescription);
    }

    const config = AGENT_TYPES[agentType] || AGENT_TYPES.coder;

    const agent = {
      id: crypto.randomBytes(8).toString('hex'),
      type: agentType,
      name: config.name,
      taskId: taskId,
      taskTitle: taskTitle,
      status: 'initializing',
      created: new Date().toISOString(),
      config: config,
      results: null,
      logs: []
    };

    this.agents.push(agent);
    this.saveAgent(agent);

    return agent;
  }

  saveAgent(agent) {
    const agentsDir = path.join(AGENTS_DIR, `session_${this.sessionId}`);
    fs.mkdirSync(agentsDir, { recursive: true });

    const agentFile = path.join(agentsDir, `agent_${agent.id}.json`);
    fs.writeFileSync(agentFile, JSON.stringify(agent, null, 2));

    // Update summary
    this.updateAgentSummary();
  }

  updateAgentSummary() {
    const agentsDir = path.join(AGENTS_DIR, `session_${this.sessionId}`);
    const summaryFile = path.join(agentsDir, 'AGENT_SUMMARY.md');

    let content = '# Agent Summary\n\n';
    content += `**Session:** ${this.sessionId}\n`;
    content += `**Total Agents:** ${this.agents.length}\n\n`;

    // Group by type
    const byType = {};
    this.agents.forEach(agent => {
      if (!byType[agent.type]) {
        byType[agent.type] = [];
      }
      byType[agent.type].push(agent);
    });

    for (const [type, agents] of Object.entries(byType)) {
      content += `## ${AGENT_TYPES[type].name}s (${agents.length})\n\n`;

      agents.forEach(agent => {
        const statusIcon =
          agent.status === 'completed' ? '✅' :
          agent.status === 'running' ? '🔄' :
          agent.status === 'failed' ? '❌' : '⏳';

        content += `### ${statusIcon} Agent ${agent.id}\n`;
        content += `- **Task:** ${agent.taskTitle}\n`;
        content += `- **Status:** ${agent.status}\n`;
        content += `- **Created:** ${agent.created}\n\n`;
      });
    }

    fs.writeFileSync(summaryFile, content);

    // Create symlink in main agents directory
    const mainSummary = path.join(AGENTS_DIR, 'AGENT_SUMMARY.md');
    if (fs.existsSync(mainSummary)) {
      fs.unlinkSync(mainSummary);
    }
    fs.symlinkSync(summaryFile, mainSummary);
  }

  updateAgentStatus(agentId, status, results = null) {
    const agent = this.agents.find(a => a.id === agentId);
    if (agent) {
      agent.status = status;
      if (results) agent.results = results;
      agent.updated = new Date().toISOString();
      this.saveAgent(agent);
    }
  }

  getAgentPrompt(agent) {
    const config = AGENT_TYPES[agent.type];
    return `${config.prompt}\n\nTask: ${agent.taskTitle}\nDescription: ${agent.taskDescription || agent.taskTitle}`;
  }

  spawnAgentsForTasks(tasks) {
    const spawned = [];

    tasks.forEach(task => {
      const agent = this.spawnAgent(
        task.id,
        task.title,
        task.description
      );
      spawned.push(agent);
    });

    console.log(`🤖 Spawned ${spawned.length} agents for parallel execution`);
    return spawned;
  }

  process(input) {
    try {
      const data = JSON.parse(input);

      // Handle task spawning requests
      if (data.type === 'spawn_agents' && data.tasks) {
        this.spawnAgentsForTasks(data.tasks);
      }

      // Handle status updates
      if (data.type === 'agent_status' && data.agentId) {
        this.updateAgentStatus(data.agentId, data.status, data.results);
      }
    } catch (e) {
      // Silent fail
    }
  }
}

// Main execution
if (process.argv[2] === 'test') {
  const spawner = new AgentSpawner();

  const testTasks = [
    { id: '1', title: 'Implement user authentication', description: 'Create login system' },
    { id: '2', title: 'Test authentication flow', description: 'Write unit tests' },
    { id: '3', title: 'Document API endpoints', description: 'Create API docs' }
  ];

  const agents = spawner.spawnAgentsForTasks(testTasks);
  console.log('Spawned agents:', agents.map(a => ({ id: a.id, type: a.type, task: a.taskTitle })));
  process.exit(0);
}

// Read input from stdin
let input = '';
process.stdin.on('data', (chunk) => (input += chunk));
process.stdin.on('end', () => {
  const spawner = new AgentSpawner();
  spawner.process(input);
  process.exit(0);
});