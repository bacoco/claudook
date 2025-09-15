#!/usr/bin/env node

/**
 * Analytics Tracker - JavaScript Version
 * Tracks tool usage for insights
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

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

const analyticsFile = path.join(root, '.claude', 'analytics.json');

function trackUsage(input) {
  try {
    const data = JSON.parse(input);

    // Load existing analytics
    let analytics = {};
    if (fs.existsSync(analyticsFile)) {
      try {
        analytics = JSON.parse(fs.readFileSync(analyticsFile, 'utf8'));
      } catch (e) {
        analytics = {};
      }
    }

    // Initialize if needed
    if (!analytics.tool_usage) analytics.tool_usage = {};
    if (!analytics.sessions) analytics.sessions = [];

    // Track tool usage
    const tool = data.tool_name || 'unknown';
    analytics.tool_usage[tool] = (analytics.tool_usage[tool] || 0) + 1;

    // Track session
    const now = new Date().toISOString();
    if (
      analytics.sessions.length === 0 ||
      new Date(now) - new Date(analytics.sessions[analytics.sessions.length - 1].last_activity) >
        3600000
    ) {
      analytics.sessions.push({
        start: now,
        last_activity: now,
        tools_used: [tool],
      });
    } else {
      const session = analytics.sessions[analytics.sessions.length - 1];
      session.last_activity = now;
      if (!session.tools_used.includes(tool)) {
        session.tools_used.push(tool);
      }
    }

    // Save analytics
    fs.writeFileSync(analyticsFile, JSON.stringify(analytics, null, 2));
  } catch (e) {
    // Silent fail
  }

  process.exit(0);
}

// Read input
let input = '';
process.stdin.on('data', (chunk) => (input += chunk));
process.stdin.on('end', () => trackUsage(input));
