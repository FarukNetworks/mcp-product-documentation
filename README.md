# MCP Product Documentation

A Model Context Protocol (MCP) server that provides access to prompt templates for software development tasks. This server makes it easy to access structured prompts for creating PRDs, SAS documents, TSDs, and more through the MCP protocol.

## Features

- 📝 **Rich Prompt Templates**: Includes templates for PRD, SAS, TSD creation and review
- 🔧 **MCP Integration**: Works seamlessly with MCP clients like Cursor IDE
- 🛡️ **Secure**: Input validation and safe file access
- 🎯 **Developer-Focused**: Designed specifically for software development workflows
- 🚀 **Easy Setup**: Simple git clone and install process

## STEP 1: Clone the repository

Clone the git repository:

```bash
git clone https://github.com/yourusername/mcp-product-documentation
```

Navigate to the mcp-product-documentation folder:

```bash
cd mcp-product-documentation
```

## STEP 2: Install dependencies

```bash
npm install
```

## STEP 3: Install the development environment

### Option A: Using npm (Recommended)

```bash
npm run dev:install
```

### Option B: Using Python installer

```bash
python3 install.py
```

Both methods will:

- Detect your Python installation
- Install required Python dependencies
- Set up the MCP server

## STEP 4: Add MCP to your agent configuration

Get the mcp.json configuration:

```bash
npm run config
```

This will output the configuration you need to add to your MCP client.

## Requirements

- **Node.js**: 14.0.0 or higher
- **Python**: 3.8 or higher (automatically detected)
- **pip**: For Python dependency installation (usually comes with Python)

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

Run `npm run config` to get the exact configuration, then add it to your `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "mcp-product-documentation": {
      "command": "node",
      "args": [
        "/path/to/your/mcp-product-documentation/bin/mcp-product-documentation.js"
      ]
    }
  }
}
```

### Other MCP Clients

The server runs as a standard MCP server using stdio transport. Use the configuration from `npm run config` for your specific MCP client.

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

## Development

### Running the Server

```bash
npm start
```

### Testing the Installation

```bash
npm run dev -- --check
```

### Running in Development Mode

```bash
npm run dev
```

### Manual Python Setup

If automatic Python dependency installation fails:

```bash
cd mcp_server
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
npm run dev:install
```

### Manual Python Dependencies

```bash
# If automatic installation fails:
python3 -m pip install mcp>=1.0.0 httpx>=0.24.0 python-multipart>=0.0.5 pydantic>=2.0.0
```

## Project Structure

```
mcp-product-documentation/
├── bin/                          # CLI executables
│   └── mcp-product-documentation.js
├── lib/                          # Library modules
│   ├── index.js                  # Main library entry
│   ├── install.js                # Installation script
│   └── config.js                 # Configuration generator
├── mcp_server/                   # Python MCP server
│   ├── prompts/                  # Prompt template files
│   ├── mcp_prompt_server.py      # Main server
│   ├── requirements.txt          # Python dependencies
│   └── tests/                    # Python tests
├── package.json                  # Node.js package configuration
└── README.md                     # This file
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
