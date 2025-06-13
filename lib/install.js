#!/usr/bin/env node

const { spawn } = require('cross-spawn');
const path = require('path');
const fs = require('fs');
const chalk = require('chalk');

// Get the directory where this package is installed
const packageDir = path.dirname(__dirname);
const requirementsPath = path.join(packageDir, 'mcp_server', 'requirements.txt');

function findPython() {
  const pythonCommands = ['python3', 'python'];

  for (const cmd of pythonCommands) {
    try {
      const result = spawn.sync(cmd, ['--version'], { stdio: 'pipe' });
      if (result.status === 0) {
        const version = result.stdout.toString();
        console.log(chalk.blue(`Found Python: ${cmd} - ${version.trim()}`));
        return cmd;
      }
    } catch (error) {
      // Continue to next command
    }
  }

  return null;
}

function checkPip(pythonCmd) {
  try {
    const result = spawn.sync(pythonCmd, ['-m', 'pip', '--version'], { stdio: 'pipe' });
    if (result.status === 0) {
      console.log(chalk.green('✓ pip is available'));
      return true;
    }
  } catch (error) {
    // pip not available
  }

  console.log(chalk.yellow('⚠ pip not found, attempting to install dependencies may fail'));
  return false;
}

function installPythonDependencies(pythonCmd) {
  console.log(chalk.blue('Installing Python dependencies...'));

  if (!fs.existsSync(requirementsPath)) {
    console.log(chalk.yellow(`Warning: requirements.txt not found at ${requirementsPath}`));
    return false;
  }

  try {
    const result = spawn.sync(pythonCmd, ['-m', 'pip', 'install', '-r', requirementsPath], {
      stdio: 'inherit',
      cwd: path.join(packageDir, 'mcp_server')
    });

    if (result.status === 0) {
      console.log(chalk.green('✓ Python dependencies installed successfully'));
      return true;
    } else {
      console.log(chalk.red('✗ Failed to install Python dependencies'));
      return false;
    }
  } catch (error) {
    console.log(chalk.red('✗ Error installing Python dependencies:'), error.message);
    return false;
  }
}

function main() {
  console.log(chalk.blue('Setting up MCP Prompt Server...'));

  // Check if we're in a CI environment or if installation should be skipped
  if (process.env.CI || process.env.SKIP_PYTHON_INSTALL) {
    console.log(chalk.yellow('Skipping Python dependency installation (CI environment or SKIP_PYTHON_INSTALL set)'));
    return;
  }

  // Find Python
  const pythonCmd = findPython();
  if (!pythonCmd) {
    console.log(chalk.red('✗ Python not found'));
    console.log(chalk.yellow('Please install Python 3.8+ to use this package.'));
    console.log(chalk.yellow('You can also set the SKIP_PYTHON_INSTALL environment variable to skip this step.'));
    process.exit(1);
  }

  // Check pip
  const hasPip = checkPip(pythonCmd);
  if (!hasPip) {
    console.log(chalk.yellow('Please ensure pip is installed to automatically install Python dependencies.'));
    console.log(chalk.yellow('You can manually install dependencies later by running:'));
    console.log(chalk.gray(`  ${pythonCmd} -m pip install -r ${requirementsPath}`));
    return;
  }

  // Install Python dependencies
  const success = installPythonDependencies(pythonCmd);
  if (success) {
    console.log(chalk.green('✓ MCP Prompt Server setup complete!'));
    console.log(chalk.blue('You can now run: mcp-product-documentation'));
  } else {
    console.log(chalk.yellow('Setup completed with warnings. You may need to manually install Python dependencies:'));
    console.log(chalk.gray(`  ${pythonCmd} -m pip install -r ${requirementsPath}`));
  }
}

// Only run if this script is executed directly (not required)
if (require.main === module) {
  main();
}

module.exports = { main }; 