# MCP Prompt Server

This server provides access to various prompt templates used by MCP agents through the Model Context Protocol (MCP).

## Setup

1.  Ensure you have Python 3.8+ installed.
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Place your prompt files (e.g., `create_prd.txt`) in a directory named `prompts` at the same level as `mcp_prompt_server.py`.

## Running the Server

### For MCP Integration (Recommended)

The server is designed to be used with MCP clients like Cursor IDE. Add this to your `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "mcp-prompt": {
      "command": "python",
      "args": ["/path/to/your/mcp_server/mcp_prompt_server.py"]
    }
  }
}
```

### For Testing/Development

You can also run the server directly for testing:

```bash
python mcp_prompt_server.py
```

## Available Tools

The MCP server provides the following tools:

### `list_available_prompts`

Lists all available prompt templates that can be fetched.

### `get_prompt_by_name`

Fetches a specific prompt template by its task name.

- **Parameters:**
  - `task_name` (string, required): The name of the task/prompt to fetch

### Individual Prompt Tools

For each prompt file, a specific tool is created:

- `get_prompt_create_prd` - Fetches the create PRD prompt
- `get_prompt_create_sas` - Fetches the create SAS prompt
- `get_prompt_review_tasks` - Fetches the review tasks prompt
- etc.

## Example Usage with MCP Clients

Once configured in your MCP client (like Cursor), you can:

1. **List available prompts:**
   "Use the list_available_prompts tool to see what templates are available."

2. **Get a specific prompt:**
   "Use get_prompt_by_name with task_name 'create_prd' to get the Product Requirements Document template."

3. **Use specific tools:**
   "Use the get_prompt_create_sas tool to get the System Architecture Specification template."

## Prompt Files

The server expects `.txt` files in the `prompts` directory. Each file should be named with the task identifier (e.g., `create_prd.txt`, `review_tasks.txt`).

## Security

- Task names are validated to prevent directory traversal attacks
- Only alphanumeric characters and underscores are allowed in task names
- File access is restricted to the designated prompts directory
