#!/usr/bin/env python3
"""
Installation script for MCP Product Documentation Server
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(
            command, shell=True, cwd=cwd, check=True, capture_output=True, text=True
        )
        print(f"✓ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {command}")
        print(f"Error: {e.stderr}")
        return False


def check_requirements():
    """Check if required tools are installed"""
    print("Checking requirements...")

    # Check Node.js
    if not run_command("node --version"):
        print("❌ Node.js is required but not found.")
        print("Please install Node.js from https://nodejs.org/")
        return False

    # Check Python
    if not run_command("python3 --version"):
        print("❌ Python 3 is required but not found.")
        print("Please install Python 3.8+ from https://python.org/")
        return False

    # Check pip
    if not run_command("python3 -m pip --version"):
        print("❌ pip is required but not found.")
        print("Please install pip with your Python installation.")
        return False

    print("✅ All requirements satisfied!")
    return True


def install_dependencies():
    """Install Node.js and Python dependencies"""
    print("\nInstalling dependencies...")

    # Install Node.js dependencies
    if not run_command("npm install"):
        print("❌ Failed to install Node.js dependencies")
        return False

    # Install Python dependencies
    if not run_command("npm run dev:install"):
        print("❌ Failed to install Python dependencies")
        return False

    print("✅ Dependencies installed successfully!")
    return True


def show_next_steps():
    """Show next steps to the user"""
    print("\n" + "=" * 50)
    print("🎉 Installation Complete!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Get MCP configuration:")
    print("   npm run config")
    print("\n2. Add the configuration to your MCP client")
    print("\n3. Start the server:")
    print("   npm start")
    print("\n4. Test in development mode:")
    print("   npm run dev")
    print("\nFor more information, see README.md")


def main():
    """Main installation function"""
    print("MCP Product Documentation Server - Installation")
    print("=" * 50)

    # Check if we're in the right directory
    if not Path("package.json").exists():
        print(
            "❌ package.json not found. Please run this script from the project root directory."
        )
        sys.exit(1)

    # Check requirements
    if not check_requirements():
        sys.exit(1)

    # Install dependencies
    if not install_dependencies():
        sys.exit(1)

    # Show next steps
    show_next_steps()


if __name__ == "__main__":
    main()
