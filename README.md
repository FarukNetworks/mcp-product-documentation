# MCP Product Documentation

A Model Context Protocol (MCP) server that provides access to prompt templates for software development tasks. This server makes it easy to access structured prompts for creating PRDs, SAS documents, TSDs, and more through the MCP protocol.

## Features

- 🚀 **Easy Installation**: Install via npm/npx with automatic Python dependency management
- 📝 **Rich Prompt Templates**: Includes templates for PRD, SAS, TSD creation and review
- 🔧 **MCP Integration**: Works seamlessly with MCP clients like Cursor IDE
- 🛡️ **Secure**: Input validation and safe file access
- 🎯 **Developer-Focused**: Designed specifically for software development workflows

## Quick Start

### Option 1: Global Installation

```bash
npm install -g mcp-product-documentation
mcp-product-documentation
```

### Option 2: Run with npx (No Installation)

```bash
npx mcp-product-documentation
```

### Option 3: Use in Project

```bash
npm install mcp-product-documentation
npx mcp-product-documentation
```

## Requirements

- **Node.js**: 14.0.0 or higher
- **Python**: 3.8 or higher (automatically detected)
- **pip**: For Python dependency installation (usually comes with Python)

The installation process will automatically:

- Detect your Python installation
- Install required Python dependencies
- Set up the MCP server

## Available Prompt Templates

The server includes the following prompt templates:

- **`create_prd`** - Product Requirements Document creation
- **`create_sas`** - System Architecture Specification creation
- **`create_tsd`** - Technical Specification Document creation
- **`review_prd`** - Product Requirements Document review
- **`review_tasks`** - Task review and validation
- **`break_prd_and_sas_to_tasks`** - Breaking down PRDs and SAS into actionable tasks

## MCP Client Integration

### Cursor IDE

Add this to your `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "mcp-prompt": {
      "command": "mcp-product-documentation"
    }
  }
}
```

### Other MCP Clients

The server runs as a standard MCP server using stdio transport. Configure your MCP client to run:

```bash
mcp-product-documentation
```

## Available Tools

Once connected to an MCP client, you'll have access to these tools:

### `list_available_prompts`

Lists all available prompt templates.

**Usage**: "List available prompts"

### `get_prompt_by_name`

Fetches a specific prompt by name.

**Parameters**:

- `task_name` (string): The name of the prompt to fetch

**Usage**: "Get the prompt for create_prd"

### Individual Prompt Tools

Each prompt has its own dedicated tool:

- `get_prompt_create_prd`
- `get_prompt_create_sas`
- `get_prompt_create_tsd`
- `get_prompt_review_prd`
- `get_prompt_review_tasks`
- `get_prompt_break_prd_and_sas_to_tasks`

## Command Line Options

```bash
mcp-product-documentation [options]

Options:
  -d, --dev              Run in development mode with verbose output
  -p, --python <path>    Path to Python executable (default: auto-detect)
  --check               Check if the server can start successfully
  -h, --help            Display help information
  -V, --version         Display version number
```

## Development

### Testing the Installation

```bash
mcp-product-documentation --check
```

### Running in Development Mode

```bash
mcp-product-documentation --dev
```

### Manual Python Setup

If automatic Python dependency installation fails:

```bash
cd node_modules/mcp-product-documentation/mcp_server  # or wherever installed
pip install -r requirements.txt
```

### Environment Variables

- `SKIP_PYTHON_INSTALL`: Set to skip automatic Python dependency installation
- `CI`: Automatically detected, skips Python installation in CI environments

## Troubleshooting

### Python Not Found

```bash
# Install Python 3.8+ from python.org or your package manager
# On macOS with Homebrew:
brew install python

# On Ubuntu/Debian:
sudo apt install python3 python3-pip

# Then retry installation
```

### Permission Issues

```bash
# On macOS/Linux, you might need:
sudo npm install -g mcp-product-documentation

# Or use a Node version manager like nvm
```

### Manual Python Dependencies

```bash
# If automatic installation fails:
python3 -m pip install mcp>=1.0.0 httpx>=0.24.0 python-multipart>=0.0.5 pydantic>=2.0.0
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/mcp-product-documentation/issues)
- **Documentation**: This README and inline code documentation
- **MCP Protocol**: [Model Context Protocol Specification](https://modelcontextprotocol.io/)

---

Made with ❤️ for the MCP community
