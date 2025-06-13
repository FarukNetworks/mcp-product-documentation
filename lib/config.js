#!/usr/bin/env node

const path = require('path');
const chalk = require('chalk');

/**
 * Generate MCP configuration for the product documentation server
 */
function generateMCPConfig() {
  const serverPath = path.resolve(__dirname, '..', 'bin', 'mcp-product-documentation.js');

  const config = {
    mcpServers: {
      "mcp-product-documentation": {
        command: "node",
        args: [serverPath]
      }
    }
  };

  return config;
}

function main() {
  console.log(chalk.blue('MCP Product Documentation Server Configuration'));
  console.log(chalk.blue('='.repeat(50)));
  console.log();

  const config = generateMCPConfig();

  console.log(chalk.green('Add this configuration to your MCP client:'));
  console.log();
  console.log(chalk.yellow('For Cursor IDE (~/.cursor/mcp.json):'));
  console.log(JSON.stringify(config, null, 2));
  console.log();

  console.log(chalk.cyan('Alternative configuration (using npm script):'));
  const altConfig = {
    mcpServers: {
      "mcp-product-documentation": {
        command: "npm",
        args: ["start"],
        cwd: path.resolve(__dirname, '..')
      }
    }
  };
  console.log(JSON.stringify(altConfig, null, 2));
  console.log();

  console.log(chalk.gray('Server location: ' + path.resolve(__dirname, '..')));
  console.log(chalk.gray('Available prompts: create_prd, create_sas, create_tsd, review_prd, review_tasks, break_prd_and_sas_to_tasks'));
}

if (require.main === module) {
  main();
}

module.exports = { generateMCPConfig }; 