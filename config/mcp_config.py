"""
MCP Server Configuration for Datadog Integration

This module handles the MCP server configuration for connecting to Datadog
through the Claude Agent SDK. It ensures the configuration is portable and
works both in development and production environments.
"""

import os
from typing import Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


def get_datadog_mcp_config() -> Dict[str, Any]:
    """
    Get the Datadog MCP server configuration for Claude Agent SDK.

    This configuration tells the Agent SDK how to spawn and connect to
    the Datadog MCP server with the appropriate credentials.

    Returns:
        Dictionary containing the MCP server configuration

    Raises:
        ValueError: If required environment variables are not set
    """
    api_key = os.getenv("DD_API_KEY")
    app_key = os.getenv("DD_APP_KEY")
    site = os.getenv("DD_SITE", "datadoghq.com")

    if not api_key or api_key == "your_datadog_api_key_here":
        raise ValueError(
            "DD_API_KEY environment variable not set. "
            "Please set it in .env file or export it."
        )

    if not app_key or app_key == "your_datadog_application_key_here":
        raise ValueError(
            "DD_APP_KEY environment variable not set. "
            "Please set it in .env file or export it."
        )

    return {
        "datadog": {
            "type": "stdio",
            "command": "datadog-mcp-server",
            "env": {
                "DD_API_KEY": api_key,
                "DD_APP_KEY": app_key,
                "DD_SITE": site,
            }
        }
    }


def get_github_mcp_config() -> Dict[str, Dict[str, Any]]:
    """
    Get GitHub MCP server configuration.

    The GitHub MCP Server provides tools for:
    - Repository management (browse code, search files, analyze commits)
    - Issue & PR automation (create, update, manage issues and PRs)
    - CI/CD & workflow intelligence (monitor Actions, analyze builds)
    - Code analysis (security findings, Dependabot alerts)
    - Team collaboration (discussions, notifications)

    Returns:
        Dictionary with GitHub MCP server configuration

    Raises:
        ValueError: If GITHUB_PERSONAL_ACCESS_TOKEN is not set
    """
    github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")

    if not github_token or github_token == "your_github_token_here":
        raise ValueError(
            "GITHUB_PERSONAL_ACCESS_TOKEN not set. "
            "Create a token at https://github.com/settings/tokens "
            "with scopes: repo, read:org, read:user, workflow"
        )

    # Path to github-mcp-server binary
    # Installed via: go install github.com/github/github-mcp-server/cmd/github-mcp-server@latest
    github_mcp_path = os.path.expanduser("~/go/bin/github-mcp-server")

    if not os.path.exists(github_mcp_path):
        raise ValueError(
            f"GitHub MCP Server not found at {github_mcp_path}. "
            "Install it with: go install github.com/github/github-mcp-server/cmd/github-mcp-server@latest"
        )

    return {
        "github": {
            "type": "stdio",
            "command": github_mcp_path,
            "args": ["stdio"],
            "env": {
                "GITHUB_PERSONAL_ACCESS_TOKEN": github_token,
            }
        }
    }


def get_all_mcp_servers() -> Dict[str, Dict[str, Any]]:
    """
    Get configuration for all MCP servers used in this project.

    This is the main function to use when initializing the Agent SDK.
    Add more MCP servers here as you expand the project (JIRA, GitHub, etc.)

    Returns:
        Dictionary of all MCP server configurations
    """
    servers = {}

    # Add Datadog MCP server
    try:
        servers.update(get_datadog_mcp_config())
    except ValueError as e:
        print(f"Warning: Could not configure Datadog MCP server: {e}")

    # Add GitHub MCP server
    try:
        servers.update(get_github_mcp_config())
    except ValueError as e:
        print(f"Warning: Could not configure GitHub MCP server: {e}")

    # Future: Add JIRA MCP server
    # servers.update(get_jira_mcp_config())

    return servers


def validate_mcp_server() -> bool:
    """
    Validate that the Datadog MCP server is installed and accessible.

    Returns:
        True if the MCP server is available, False otherwise
    """
    import shutil

    mcp_server_path = shutil.which("datadog-mcp-server")

    if not mcp_server_path:
        print("Error: datadog-mcp-server not found in PATH")
        print("Install it with: npm install -g datadog-mcp-server")
        return False

    print(f"Found datadog-mcp-server at: {mcp_server_path}")
    return True


# Legacy functions - not needed for Claude Agent SDK
# These were used with the old MCP client, but Claude Agent SDK uses dict format


if __name__ == "__main__":
    # Test the configuration
    print("Testing MCP Configuration...")
    print("-" * 50)

    if validate_mcp_server():
        print("\nMCP Server: OK")

    try:
        config = get_datadog_mcp_config()
        print("\nDatadog MCP Configuration (dict format):")
        print(f"  Command: {config['datadog']['command']}")
        print(f"  Site: {config['datadog']['env']['DD_SITE']}")
        print(f"  API Key: {'*' * 20} (hidden)")
        print(f"  App Key: {'*' * 20} (hidden)")
        print("\nConfiguration: OK")

    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
