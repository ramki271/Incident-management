#!/usr/bin/env python3
"""
Autonomous Agent with Claude Agent SDK + MCP Integration

This agent uses the official Claude Agent SDK to autonomously decide which MCP tools to call
based on natural language queries. Claude sees all available MCP tools and
intelligently chooses which ones to use.

The Claude Agent SDK provides:
- Automatic tool calling and result handling
- Built-in agentic loop
- Context management and compaction
- Support for hooks and subagents
"""

import os
import sys
import anyio
from typing import Dict, Any, Optional

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, query as sdk_query
from config.mcp_config import get_all_mcp_servers, validate_mcp_server


class AutonomousAgent:
    """
    Autonomous agent that uses Claude Agent SDK + MCP tools.

    Claude autonomously decides which MCP tools to call based on the query.
    Supports multiple MCP servers (Datadog, JIRA, GitHub, etc.).

    This is a wrapper around the Claude Agent SDK that provides a simpler interface
    similar to the old manual implementation.
    """

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize the Autonomous Agent.

        Args:
            model: Claude model to use

        Raises:
            ValueError: If ANTHROPIC_API_KEY is not set
            RuntimeError: If MCP servers not found
        """
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable not set. "
                "Get your API key from: https://console.anthropic.com/"
            )

        self.model = model

        # Validate MCP server is available
        if not validate_mcp_server():
            raise RuntimeError(
                "Datadog MCP server not found. "
                "Install with: npm install -g datadog-mcp-server"
            )

        # Get MCP server configurations
        mcp_servers = get_all_mcp_servers()

        # Create Claude Agent SDK options
        # Note: API key is read from ANTHROPIC_API_KEY environment variable by the SDK
        self.options = ClaudeAgentOptions(
            model=model,
            mcp_servers=mcp_servers,
            permission_mode="bypassPermissions"  # Auto-accept all tool calls for autonomous operation
        )

        self.client: Optional[ClaudeSDKClient] = None

        print(f"AutonomousAgent initialized with model: {model}")
        print(f"MCP Servers configured: {list(mcp_servers.keys())}")

    async def start(self):
        """Start the Claude SDK client."""
        self.client = ClaudeSDKClient(options=self.options)
        await self.client.__aenter__()
        print("Claude Agent SDK client started")

    async def stop(self):
        """Stop the Claude SDK client."""
        if self.client:
            await self.client.__aexit__(None, None, None)
            self.client = None
        print("Claude Agent SDK client stopped")

    async def query(self, prompt: str, max_tokens: int = 4096, verbose: bool = True) -> str:
        """
        Send a query to Claude with MCP tool access using the Claude Agent SDK.

        Claude will autonomously decide which tools to call and synthesize a response.

        Args:
            prompt: Natural language query
            max_tokens: Maximum tokens in response
            verbose: Print detailed execution info

        Returns:
            Claude's response after using tools
        """
        if not self.client:
            raise RuntimeError("Client not started. Call start() first or use async context manager.")

        if verbose:
            print(f"\n{'='*70}")
            print(f"Query: {prompt}")
            print(f"{'='*70}\n")

        # Send query to Claude Agent SDK
        await self.client.query(prompt)

        # Collect response
        response_text = ""
        async for message in self.client.receive_response():
            if verbose:
                print(message)
            # Collect text from the response
            if hasattr(message, 'content'):
                for block in message.content:
                    if hasattr(block, 'text'):
                        response_text += block.text

        if verbose:
            print(f"\n{'='*70}")
            print(f"Final Response:")
            print(f"{'='*70}")
            print(response_text)
            print(f"{'='*70}\n")

        return response_text

    async def __aenter__(self):
        """Async context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.stop()
        return False


async def simple_query(prompt: str, verbose: bool = True) -> str:
    """
    Simple one-off query using the Claude Agent SDK.

    This is a convenience function for quick queries without managing the agent lifecycle.

    Args:
        prompt: Natural language query
        verbose: Print detailed execution info

    Returns:
        Claude's response after using tools
    """
    # Get MCP server configurations
    mcp_servers = get_all_mcp_servers()

    # Use the SDK's query function directly
    response_text = ""
    async for message in sdk_query(prompt=prompt, mcp_servers=mcp_servers):
        if verbose:
            print(message)
        # Collect text from the response
        if hasattr(message, 'content'):
            for block in message.content:
                if hasattr(block, 'text'):
                    response_text += block.text

    return response_text


async def main():
    """Example usage of AutonomousAgent with Claude Agent SDK."""
    print("="*70)
    print("Autonomous Agent - Claude Agent SDK + MCP Integration")
    print("="*70)

    try:
        # Use async context manager for automatic cleanup
        async with AutonomousAgent() as agent:

            # Example 1: Simple query that requires one tool
            print("\n[Example 1] Simple Query")
            print("-"*70)
            await agent.query(
                "How many Datadog monitors do I have in alert state?",
                verbose=True
            )

            # Example 2: Complex query that might require multiple tools
            print("\n\n[Example 2] Complex Query")
            print("-"*70)
            await agent.query(
                "Show me the 3 most critical issues in my Datadog monitoring. "
                "Look at monitors in alert state and tell me what's wrong.",
                verbose=True
            )

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    anyio.run(main)
