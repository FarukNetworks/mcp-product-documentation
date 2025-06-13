#!/usr/bin/env python3
"""
MCP Product Documentation Server - Configuration Generator

This script generates the MCP configuration that you need to add to your MCP client.
"""

import json
import os
import subprocess
import sys
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


def install_dependencies():
    """Install Python dependencies if not already installed"""
    requirements_file = Path(__file__).parent / "mcp_server" / "requirements.txt"

    if not requirements_file.exists():
        print("⚠️  Warning: requirements.txt not found")
        return False

    print("🔧 Installing Python dependencies...")
    try:
        # Install dependencies
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        print("✅ Dependencies installed successfully!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print(f"Error output: {e.stderr}")
        print("\n💡 Try installing manually:")
        print(f"   cd mcp_server")
        print(f"   pip3 install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def check_dependencies():
    """Check if MCP dependencies are installed"""
    try:
        import mcp

        return True
    except ImportError:
        return False


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

    # Check and install dependencies if needed
    if not check_dependencies():
        print("📦 MCP dependencies not found. Installing...")
        if not install_dependencies():
            print(
                "\n❌ Setup failed. Please install dependencies manually and try again."
            )
            return
        print()

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
