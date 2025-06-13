const { main: installDependencies } = require('./install');
const path = require('path');

/**
 * MCP Prompt Server Library
 * 
 * This module provides programmatic access to the MCP Prompt Server functionality.
 */

/**
 * Get the path to the Python server script
 * @returns {string} Path to the mcp_prompt_server.py file
 */
function getServerPath() {
  return path.join(__dirname, '..', 'mcp_server', 'mcp_prompt_server.py');
}

/**
 * Get the path to the prompts directory
 * @returns {string} Path to the prompts directory
 */
function getPromptsPath() {
  return path.join(__dirname, '..', 'mcp_server', 'prompts');
}

/**
 * Get the path to the requirements.txt file
 * @returns {string} Path to the requirements.txt file
 */
function getRequirementsPath() {
  return path.join(__dirname, '..', 'mcp_server', 'requirements.txt');
}

/**
 * Install Python dependencies programmatically
 * @returns {Promise<void>}
 */
async function install() {
  return installDependencies();
}

module.exports = {
  getServerPath,
  getPromptsPath,
  getRequirementsPath,
  install
}; 