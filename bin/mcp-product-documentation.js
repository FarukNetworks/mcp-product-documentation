#!/usr/bin/env node

const { program } = require('commander');
const { spawn } = require('cross-spawn');
const path = require('path');
const fs = require('fs');
const chalk = require('chalk');

// Get the directory where this package is installed
const packageDir = path.dirname(__dirname);
const serverPath = path.join(packageDir, 'mcp_server', 'mcp_prompt_server.py');

program
  .name('mcp-product-documentation')
  .description('MCP Product Documentation - Provides access to prompt templates via Model Context Protocol')
  .version('1.0.0')
  .option('-d, --dev', 'Run in development mode with verbose output')
  .option('-p, --python <path>', 'Path to Python executable (default: python3 or python)')
  .option('--check', 'Check if the server can start successfully')
  .parse();

const options = program.opts();

function findPython() {
  const pythonCommands = ['python3', 'python'];

  for (const cmd of pythonCommands) {
    try {
      const result = spawn.sync(cmd, ['--version'], { stdio: 'pipe' });
      if (result.status === 0) {
        const version = result.stdout.toString();
        if (options.dev) {
          console.log(chalk.blue(`Found Python: ${cmd} - ${version.trim()}`));
        }
        return cmd;
      }
    } catch (error) {
      // Continue to next command
    }
  }

  throw new Error('Python not found. Please install Python 3.8+ or specify path with --python');
}

function checkServerFile() {
  if (!fs.existsSync(serverPath)) {
    console.error(chalk.red(`Error: Server file not found at ${serverPath}`));
    console.error(chalk.yellow('This might indicate a corrupted installation. Try reinstalling the package.'));
    process.exit(1);
  }
}

function checkPromptsDirectory() {
  const promptsDir = path.join(packageDir, 'mcp_server', 'prompts');
  if (!fs.existsSync(promptsDir)) {
    console.error(chalk.red(`Error: Prompts directory not found at ${promptsDir}`));
    process.exit(1);
  }

  const promptFiles = fs.readdirSync(promptsDir).filter(file => file.endsWith('.txt'));
  if (options.dev) {
    console.log(chalk.green(`Found ${promptFiles.length} prompt files: ${promptFiles.join(', ')}`));
  }

  return promptFiles.length;
}

async function runServer() {
  try {
    // Validate installation
    checkServerFile();
    const promptCount = checkPromptsDirectory();

    // Find Python executable
    const pythonCmd = options.python || findPython();

    if (options.check) {
      console.log(chalk.green('✓ Server files found'));
      console.log(chalk.green(`✓ Python found: ${pythonCmd}`));
      console.log(chalk.green(`✓ ${promptCount} prompt templates available`));
      console.log(chalk.blue('Server appears to be properly installed and ready to run.'));
      return;
    }

    if (options.dev) {
      console.log(chalk.blue('Starting MCP Prompt Server...'));
      console.log(chalk.gray(`Server path: ${serverPath}`));
      console.log(chalk.gray(`Python command: ${pythonCmd}`));
    }

    // Start the Python server
    const serverProcess = spawn(pythonCmd, [serverPath], {
      stdio: 'inherit',
      cwd: path.join(packageDir, 'mcp_server')
    });

    // Handle process termination
    process.on('SIGINT', () => {
      if (options.dev) {
        console.log(chalk.yellow('\nShutting down server...'));
      }
      serverProcess.kill('SIGINT');
    });

    process.on('SIGTERM', () => {
      serverProcess.kill('SIGTERM');
    });

    serverProcess.on('exit', (code) => {
      if (code !== 0 && code !== null) {
        console.error(chalk.red(`Server exited with code ${code}`));
        process.exit(code);
      }
    });

    serverProcess.on('error', (error) => {
      console.error(chalk.red('Failed to start server:'), error.message);
      process.exit(1);
    });

  } catch (error) {
    console.error(chalk.red('Error:'), error.message);
    process.exit(1);
  }
}

// Run the server
runServer(); 