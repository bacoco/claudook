# claudook/help

Show all available Claudook commands and their descriptions.

## Usage
Use `/claudook/help` to see this comprehensive list of all Claudook features and commands.

## Available Commands

### Status & Information
- `/claudook/status` - Show current Claudook configuration and active features
- `/claudook/task-status` - Display current task execution status and progress
- `/claudook/version` - Show installed Claudook version

### Feature Toggles
- `/claudook/choices-enable` - Enable A/B/C multiple choice options for complex tasks
- `/claudook/choices-disable` - Disable multiple choice options
- `/claudook/tests-enable` - Enable mandatory test enforcement before code changes
- `/claudook/tests-disable` - Disable mandatory test enforcement
- `/claudook/parallel-enable` - Enable parallel task execution
- `/claudook/parallel-disable` - Disable parallel task execution

### Security & Quality
- `/claudook/security-check` - Run security analysis on current code
- `/claudook/performance-check` - Analyze performance bottlenecks
- `/claudook/lint` - Run linting and code quality checks

### Configuration
- `/claudook/config-show` - Display all configuration settings
- `/claudook/config-reset` - Reset to default configuration
- `/claudook/update` - Check for and install Claudook updates
- `/claudook/uninstall` - Remove Claudook from current project

## Quick Start
1. Check status: `/claudook/status`
2. Enable features: `/claudook/choices-enable` or `/claudook/tests-enable`
3. Run checks: `/claudook/security-check` or `/claudook/performance-check`

For more information, visit: https://github.com/bacoco/claudook