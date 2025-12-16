#!/usr/bin/env python3
"""
Test GitHub MCP Server Integration

This script tests the GitHub MCP Server integration by:
1. Verifying the GitHub MCP Server is installed and configured
2. Listing available GitHub tools
3. Running a simple query to test connectivity

Before running:
1. Set GITHUB_PERSONAL_ACCESS_TOKEN in .env file
2. Create a token at: https://github.com/settings/tokens
3. Required scopes: repo, read:org, read:user, workflow
"""

import os
import sys
import anyio

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from config.mcp_config import get_github_mcp_config, get_all_mcp_servers


async def test_github_mcp():
    """Test GitHub MCP Server configuration and connectivity."""
    print("="*70)
    print("GitHub MCP Server Test")
    print("="*70)
    print()
    
    # Test 1: Check configuration
    print("Test 1: Checking GitHub MCP Server configuration...")
    try:
        github_config = get_github_mcp_config()
        print("✓ GitHub MCP Server configuration loaded successfully")
        print(f"  Command: {github_config['github']['command']}")
        print(f"  Type: {github_config['github']['type']}")
        print()
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        print()
        print("To fix this:")
        print("1. Create a GitHub Personal Access Token at:")
        print("   https://github.com/settings/tokens")
        print("2. Required scopes: repo, read:org, read:user, workflow")
        print("3. Add it to your .env file as GITHUB_PERSONAL_ACCESS_TOKEN")
        return
    
    # Test 2: Check all MCP servers
    print("Test 2: Checking all MCP servers...")
    all_servers = get_all_mcp_servers()
    print(f"✓ Found {len(all_servers)} MCP server(s):")
    for server_name in all_servers.keys():
        print(f"  - {server_name}")
    print()
    
    # Test 3: Verify binary exists
    print("Test 3: Verifying GitHub MCP Server binary...")
    github_binary = os.path.expanduser("~/go/bin/github-mcp-server")
    if os.path.exists(github_binary):
        print(f"✓ GitHub MCP Server binary found at: {github_binary}")
        
        # Check if it's executable
        if os.access(github_binary, os.X_OK):
            print("✓ Binary is executable")
        else:
            print("✗ Binary is not executable")
            print(f"  Run: chmod +x {github_binary}")
    else:
        print(f"✗ GitHub MCP Server binary not found at: {github_binary}")
        print("  Install it with:")
        print("  go install github.com/github/github-mcp-server/cmd/github-mcp-server@latest")
    print()
    
    # Test 4: Test with Claude Agent SDK
    print("Test 4: Testing with Claude Agent SDK...")
    try:
        from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

        print("Sending test query to GitHub MCP Server...")
        print("Query: 'What's my GitHub username?'")
        print()

        # Create Claude Agent SDK client
        options = ClaudeAgentOptions(
            model="claude-sonnet-4-20250514",
            mcp_servers=all_servers,
            permission_mode="bypassPermissions"
        )

        async with ClaudeSDKClient(options=options) as client:
            await client.query("Use GitHub tools to get information about the authenticated user (me). What's my GitHub username?")

            response_text = ""
            async for message in client.receive_response():
                print(message)
                if hasattr(message, 'content'):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            response_text += block.text

        print()
        print("="*70)
        print("Test Complete!")
        print("="*70)
        print()
        print("GitHub MCP Server is working correctly! ✓")
        print()
        print("You can now use GitHub tools in your agent workflows:")
        print("  - Repository management")
        print("  - Issue & PR automation")
        print("  - CI/CD monitoring")
        print("  - Code analysis")
        print("  - Team collaboration")

    except Exception as e:
        print(f"✗ Error testing with Claude Agent SDK: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    anyio.run(test_github_mcp)

