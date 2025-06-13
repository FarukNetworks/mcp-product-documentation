#!/usr/bin/env python3
"""
MCP Product Documentation Server - Configuration Generator

This script generates the MCP configuration that you need to add to your MCP client.
"""

import json
import os
from pathlib import Path


def generate_mcp_config():
    """Generate MCP configuration for the product documentation server"""

    # Get the absolute path to the server script
    current_dir = Path(__file__).parent.absolute()
    server_script = current_dir / "mcp_server" / "mcp_prompt_server.py"

    # Check if server script exists
    if not server_script.exists():
        print(f"❌ Error: Server script not found at {server_script}")
        print("Make sure you're running this from the project root directory.")
        return None

    # Generate the configuration
    config = {
        "mcpServers": {
            "mcp-product-documentation": {
                "command": "python3",
                "args": [str(server_script)],
            }
        }
    }

    return config, str(current_dir)


def check_prompts():
    """Check available prompt templates"""
    prompts_dir = Path(__file__).parent / "mcp_server" / "prompts"

    if not prompts_dir.exists():
        return []

    prompt_files = list(prompts_dir.glob("*.txt"))
    return [f.stem for f in prompt_files]


def main():
    """Main function"""
    print("🚀 MCP Product Documentation Server")
    print("=" * 50)

    # Generate configuration
    result = generate_mcp_config()
    if not result:
        return

    config, project_path = result

    # Check available prompts
    prompts = check_prompts()

    print(f"📁 Project location: {project_path}")
    print(f"📝 Available prompts: {len(prompts)}")
    if prompts:
        for prompt in sorted(prompts):
            print(f"   • {prompt}")

    print("\n" + "=" * 50)
    print("📋 MCP Configuration")
    print("=" * 50)
    print("\nCopy this configuration to your MCP client:")
    print("\n🔸 For Cursor IDE (~/.cursor/mcp.json):")
    print(json.dumps(config, indent=2))

    print("\n" + "=" * 50)
    print("✅ Setup Complete!")
    print("=" * 50)
    print("\n1. Copy the configuration above")
    print("2. Add it to your MCP client configuration file")
    print("3. Restart your MCP client")
    print("4. You can now use the prompt tools!")

    print(f"\n💡 Server will run from: {project_path}")


if __name__ == "__main__":
    main()
