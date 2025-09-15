#!/usr/bin/env node

import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs-extra';
import chalk from 'chalk';
const { blue, green, red, yellow, cyan } = chalk;
import inquirer from 'inquirer';
import { execSync } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const packageRoot = join(__dirname, '..');

const banner = chalk.blue(`
   ______ _                 _             _
  / _____| |               | |           | |
 | |     | | __ _ _   _  __| | ___   ___ | | __
 | |     | |/ _\` | | | |/ _\` |/ _ \\ / _ \\| |/ /
 | |_____| | (_| | |_| | (_| | (_) | (_) |   <
  \\______|_|\\__,_|\\__,_|\\__,_|\\___/ \\___/|_|\\_\\

  ${chalk.cyan('Pure JavaScript Claude Enhancement')}
`);

async function checkNodeVersion() {
  const nodeVersion = process.version;
  const major = parseInt(nodeVersion.split('.')[0].substring(1));

  if (major < 14) {
    console.error(chalk.red(`❌ Node.js 14+ required (you have ${nodeVersion})`));
    console.log(chalk.yellow('Please upgrade Node.js: https://nodejs.org'));
    process.exit(1);
  }

  console.log(chalk.green(`✅ Node.js ${nodeVersion} detected`));
}

async function checkInstallLocation() {
  const cwd = process.cwd();
  const homeDir = process.env.HOME || process.env.USERPROFILE;

  if (cwd === join(homeDir, '.claude') || cwd === homeDir) {
    console.error(chalk.red('❌ Cannot install in global Claude directory!'));
    console.log(chalk.yellow('Please navigate to your project directory first.'));
    process.exit(1);
  }

  return cwd;
}

async function confirmInstallation(installDir) {
  console.log(chalk.blue(`📁 Installing to: ${chalk.cyan(installDir)}`));

  const answers = await inquirer.prompt([
    {
      type: 'confirm',
      name: 'proceed',
      message: 'Install Claudook in this directory?',
      default: true
    }
  ]);

  if (!answers.proceed) {
    console.log(chalk.yellow('Installation cancelled.'));
    process.exit(0);
  }
}

async function copyHookFiles(installDir) {
  const sourceDir = join(packageRoot, '.claude');
  const targetDir = join(installDir, '.claude');

  console.log(chalk.blue('🔧 Installing hooks...'));

  // Create directories
  await fs.ensureDir(join(targetDir, 'hooks', 'claudook'));
  await fs.ensureDir(join(targetDir, 'commands', 'claudook'));

  // Copy JavaScript hooks
  const hooksSource = join(sourceDir, 'hooks', 'claudook');
  const hooksTarget = join(targetDir, 'hooks', 'claudook');

  const hookFiles = await fs.readdir(hooksSource);
  for (const file of hookFiles) {
    if (file.endsWith('.js')) {
      await fs.copy(
        join(hooksSource, file),
        join(hooksTarget, file)
      );
    }
  }

  console.log(chalk.green('✅ Hooks installed'));

  // Copy commands
  const commandsSource = join(sourceDir, 'commands', 'claudook');
  const commandsTarget = join(targetDir, 'commands', 'claudook');

  if (await fs.pathExists(commandsSource)) {
    await fs.copy(commandsSource, commandsTarget);
    console.log(chalk.green('✅ Commands installed'));
  }
}

async function createSettings(installDir) {
  const settingsPath = join(installDir, '.claude', 'settings.json');

  if (await fs.pathExists(settingsPath)) {
    const timestamp = Date.now();
    const backupPath = `${settingsPath}.backup.${timestamp}`;
    await fs.copy(settingsPath, backupPath);
    console.log(chalk.yellow(`💾 Backed up existing settings to ${backupPath}`));
  }

  const settings = {
    hooks: {
      before_tool_use: [
        {
          hooks: [
            {
              command: "node .claude/hooks/claudook/security_guard.js",
              args: ["${tool_name}", "${params}"],
              blocking: true
            },
            {
              command: "node .claude/hooks/claudook/analytics_tracker.js",
              args: ["before", "${tool_name}", "${params}"],
              blocking: false
            }
          ]
        }
      ],
      after_tool_use: [
        {
          hooks: [
            {
              command: "node .claude/hooks/claudook/analytics_tracker.js",
              args: ["after", "${tool_name}", "${result}"],
              blocking: false
            }
          ]
        }
      ]
    }
  };

  await fs.writeJson(settingsPath, settings, { spaces: 2 });
  console.log(chalk.green('✅ Settings configured'));
}

async function setupPackageJson(installDir) {
  const packagePath = join(installDir, 'package.json');
  let pkg = {};

  if (await fs.pathExists(packagePath)) {
    pkg = await fs.readJson(packagePath);
  } else {
    pkg = {
      name: "claudook-project",
      version: "1.0.0",
      private: true
    };
  }

  // Add Claudook dependencies
  pkg.dependencies = pkg.dependencies || {};
  pkg.dependencies['chalk'] = '^5.3.0';
  pkg.dependencies['fs-extra'] = '^11.1.1';

  // Add scripts
  pkg.scripts = pkg.scripts || {};
  pkg.scripts['claudook:test'] = 'node .claude/hooks/claudook/security_guard.js test';
  pkg.scripts['claudook:status'] = 'node .claude/hooks/claudook/analytics_tracker.js status';

  await fs.writeJson(packagePath, pkg, { spaces: 2 });
  console.log(chalk.green('✅ package.json updated'));

  // Install dependencies
  console.log(chalk.blue('📦 Installing dependencies...'));
  try {
    execSync('npm install', { cwd: installDir, stdio: 'inherit' });
    console.log(chalk.green('✅ Dependencies installed'));
  } catch (error) {
    console.log(chalk.yellow('⚠️ npm install failed, you may need to run it manually'));
  }
}

async function createFeatureFlags(installDir) {
  const claudeDir = join(installDir, '.claude');

  await fs.ensureFile(join(claudeDir, 'choices_enabled'));
  await fs.ensureFile(join(claudeDir, 'tests_enabled'));

  console.log(chalk.green('✅ Feature flags enabled'));
}

async function createClaudeMd(installDir) {
  const content = `# Claudook Configuration - Pure JavaScript Edition

This project has Claudook installed locally in the \`.claude/\` directory.
**No Python dependencies required - runs on pure Node.js!**

## Quick Commands
- \`/claudook/status\` - Check hook status
- \`/claudook/help\` - Show all available commands
- \`/claudook/choices-enable\` - Enable A/B/C options
- \`/claudook/tests-enable\` - Enable test enforcement

## Testing
\`\`\`bash
npm run claudook:test    # Test hooks
npm run claudook:status  # Check status
\`\`\`

## Features
✅ Multiple Choice System (A/B/C options)
✅ Test Enforcement (mandatory tests)
✅ Security Guards (blocks dangerous operations)
✅ Performance Optimization
✅ Documentation Enforcement

---
Installed with npx create-claudook
`;

  await fs.writeFile(join(installDir, 'CLAUDE.md'), content);
  console.log(chalk.green('✅ CLAUDE.md created'));
}

async function main() {
  console.clear();
  console.log(banner);
  console.log(chalk.magenta('🚀 Installing Claudook...\n'));

  try {
    await checkNodeVersion();
    const installDir = await checkInstallLocation();
    await confirmInstallation(installDir);

    console.log();
    await copyHookFiles(installDir);
    await createSettings(installDir);
    await setupPackageJson(installDir);
    await createFeatureFlags(installDir);
    await createClaudeMd(installDir);

    console.log();
    console.log(chalk.green.bold('🎉 Installation Complete!\n'));
    console.log(chalk.cyan('This is a LOCAL installation:'));
    console.log(`  • Files are in ${chalk.yellow(join(installDir, '.claude'))}`);
    console.log('  • Settings are project-specific');
    console.log('  • Works immediately (no restart needed)\n');

    // Check if package.json exists and has dependencies
    const packageJsonPath = join(installDir, 'package.json');
    if (await fs.pathExists(packageJsonPath)) {
      const packageJson = await fs.readJson(packageJsonPath);
      if ((packageJson.dependencies && Object.keys(packageJson.dependencies).length > 0) ||
          (packageJson.devDependencies && Object.keys(packageJson.devDependencies).length > 0)) {
        console.log(chalk.yellow.bold('⚠️  Important: Run npm install\n'));
        console.log(chalk.yellow('Your project has npm dependencies. Please run:'));
        console.log(chalk.cyan('  npm install\n'));
      }
    }

    console.log(chalk.magenta('🚀 Try it out:'));
    console.log('  Ask Claude to create a feature and watch the automation!\n');

  } catch (error) {
    console.error(chalk.red('❌ Installation failed:'), error.message);
    process.exit(1);
  }
}

main();