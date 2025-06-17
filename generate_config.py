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

    # Try different installation methods in order of preference
    install_methods = [
        # Method 1: User installation (safest)
        {
            "args": [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--user",
                "-r",
                str(requirements_file),
            ],
            "description": "user installation",
        },
        # Method 2: Break system packages (if user allows)
        {
            "args": [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--break-system-packages",
                "-r",
                str(requirements_file),
            ],
            "description": "system-wide installation",
        },
    ]

    for method in install_methods:
        try:
            print(f"   Trying {method['description']}...")
            result = subprocess.run(
                method["args"], capture_output=True, text=True, check=True
            )
            print("✅ Dependencies installed successfully!")
            return True

        except subprocess.CalledProcessError as e:
            if "externally-managed-environment" in e.stderr:
                print(f"   ⚠️  {method['description']} blocked by system policy")
                continue
            else:
                print(f"   ❌ {method['description']} failed: {e}")
                continue
        except Exception as e:
            print(f"   ❌ Unexpected error with {method['description']}: {e}")
            continue

    # If all methods failed, provide helpful instructions
    print("\n❌ Automatic installation failed. Please install manually:")
    print("\n🔧 Option 1 - User installation (recommended):")
    print(f"   cd mcp_server")
    print(f"   python3 -m pip install --user -r requirements.txt")

    print("\n🔧 Option 2 - Virtual environment (safest):")
    print(f"   python3 -m venv venv")
    print(f"   source venv/bin/activate")
    print(f"   pip install -r mcp_server/requirements.txt")
    print(f"   # Then run: python3 generate_config.py")

    print("\n🔧 Option 3 - System override (use with caution):")
    print(f"   cd mcp_server")
    print(f"   python3 -m pip install --break-system-packages -r requirements.txt")

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
