#!/usr/bin/env python3
"""
MCP Prompt Server

A Model Context Protocol server that provides access to prompt templates.
This server implements the MCP specification to serve prompts as tools.
"""

import asyncio
import json
import re
from pathlib import Path
from typing import Any, Dict, List

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    TextContent,
    Tool,
)

# Configuration
PROMPTS_DIR = Path(__file__).parent / "prompts"

# Create the MCP server
app = Server("mcp-product-documentation")


def is_safe_task_name(task_name: str) -> bool:
    """
    Validates the task name to prevent directory traversal and ensure it's a simple string.
    Allows alphanumeric characters and underscores.
    """
    if not task_name:
        return False
    if re.fullmatch(r"[a-zA-Z0-9_]+", task_name) and ".." not in task_name:
        return True
    return False


def get_available_prompts() -> List[str]:
    """
    Returns a list of available prompt task names by scanning the prompts directory.
    """
    if not PROMPTS_DIR.exists() or not PROMPTS_DIR.is_dir():
        return []

    prompt_files = []
    for file_path in PROMPTS_DIR.glob("*.txt"):
        # Remove the .txt extension to get the task name
        task_name = file_path.stem
        if is_safe_task_name(task_name):
            prompt_files.append(task_name)

    return sorted(prompt_files)


def read_prompt_content(task_name: str) -> str:
    """
    Reads the content of a specific prompt file.
    """
    if not is_safe_task_name(task_name):
        raise ValueError(f"Invalid task name: {task_name}")

    prompt_file_path = PROMPTS_DIR / f"{task_name}.txt"

    if not prompt_file_path.exists() or not prompt_file_path.is_file():
        raise FileNotFoundError(f"Prompt not found for task: {task_name}")

    try:
        with open(prompt_file_path, "r", encoding="utf-8") as f:
            return f.read()
    except IOError as e:
        raise IOError(f"Error reading prompt file for task: {task_name}") from e


@app.list_tools()
async def list_tools() -> List[Tool]:
    """
    List all available prompt tools.
    Each prompt file becomes a tool that can be called.
    """
    available_prompts = get_available_prompts()

    tools = []

    # Add a tool to list all available prompts
    tools.append(
        Tool(
            name="list_available_prompts",
            description="Lists all available prompt templates that can be fetched. Use this to discover what prompts are available.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        )
    )

    # Add a tool for each prompt
    for prompt_name in available_prompts:
        tools.append(
            Tool(
                name=f"get_prompt_{prompt_name}",
                description=f"Fetches the '{prompt_name}' prompt template. This provides a structured template for {prompt_name.replace('_', ' ')} tasks.",
                inputSchema={"type": "object", "properties": {}, "required": []},
            )
        )

    # Add a generic tool to get any prompt by name
    tools.append(
        Tool(
            name="get_prompt_by_name",
            description="Fetches a specific prompt template by its task name. Use this when you know the exact name of the prompt you want.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_name": {
                        "type": "string",
                        "description": "The name of the task/prompt to fetch (e.g., 'create_prd', 'review_tasks')",
                    }
                },
                "required": ["task_name"],
            },
        )
    )

    return tools


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """
    Handle tool calls for prompt fetching.
    """
    try:
        if name == "list_available_prompts":
            available_prompts = get_available_prompts()
            prompt_list = "\n".join([f"- {prompt}" for prompt in available_prompts])
            return [
                TextContent(
                    type="text",
                    text=f"Available prompts:\n{prompt_list}\n\nUse 'get_prompt_by_name' with the task_name parameter, or use the specific 'get_prompt_[name]' tools to fetch individual prompts.",
                )
            ]

        elif name == "get_prompt_by_name":
            task_name = arguments.get("task_name")
            if not task_name:
                return [
                    TextContent(
                        type="text", text="Error: task_name parameter is required"
                    )
                ]

            try:
                prompt_content = read_prompt_content(task_name)
                return [
                    TextContent(
                        type="text",
                        text=f"Prompt for '{task_name}':\n\n{prompt_content}",
                    )
                ]
            except (ValueError, FileNotFoundError, IOError) as e:
                return [TextContent(type="text", text=f"Error: {str(e)}")]

        elif name.startswith("get_prompt_"):
            # Extract task name from tool name (e.g., "get_prompt_create_prd" -> "create_prd")
            task_name = name[len("get_prompt_") :]

            try:
                prompt_content = read_prompt_content(task_name)
                return [
                    TextContent(
                        type="text",
                        text=f"Prompt for '{task_name}':\n\n{prompt_content}",
                    )
                ]
            except (ValueError, FileNotFoundError, IOError) as e:
                return [TextContent(type="text", text=f"Error: {str(e)}")]

        else:
            return [TextContent(type="text", text=f"Error: Unknown tool '{name}'")]

    except Exception as e:
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]


async def main():
    """
    Main entry point for the MCP server.
    """
    # Ensure prompts directory exists
    if not PROMPTS_DIR.exists():
        print(f"Error: Prompts directory not found at {PROMPTS_DIR}")
        print("Please create it and add your .txt prompt files there.")
        return

    if not PROMPTS_DIR.is_dir():
        print(f"Error: {PROMPTS_DIR} is not a directory.")
        return

    print(f"MCP Prompt Server starting. Prompts directory: {PROMPTS_DIR.resolve()}")
    available_prompts = get_available_prompts()
    print(f"Found {len(available_prompts)} prompts: {', '.join(available_prompts)}")

    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
