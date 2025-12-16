# How to Add New MCP Servers

## The Simple 3-Step Pattern

All MCP server additions happen in **`config/mcp_config.py`**. No other files need to be modified!

## Step-by-Step Guide

### Step 1: Create a Configuration Function

Add a new function following this pattern:

```python
def get_<server_name>_mcp_config() -> Dict[str, Dict[str, Any]]:
    """
    Get <Server Name> MCP server configuration.
    
    The <Server Name> MCP Server provides tools for:
    - Feature 1
    - Feature 2
    - Feature 3
    
    Returns:
        Dictionary with <Server Name> MCP server configuration
        
    Raises:
        ValueError: If required credentials are not set
    """
    # 1. Get credentials from environment
    api_key = os.getenv("SERVER_API_KEY")
    
    # 2. Validate credentials
    if not api_key:
        raise ValueError(
            "SERVER_API_KEY not set. "
            "Get your API key from: https://..."
        )
    
    # 3. Return MCP server configuration
    return {
        "server_name": {
            "type": "stdio",  # or "http" for remote servers
            "command": "path-to-mcp-server-binary",
            "args": ["arg1", "arg2"],  # optional
            "env": {
                "API_KEY": api_key,
                # Add other environment variables
            }
        }
    }
```

### Step 2: Enable in `get_all_mcp_servers()`

Add your server to the `get_all_mcp_servers()` function:

```python
def get_all_mcp_servers() -> Dict[str, Dict[str, Any]]:
    """
    Get configuration for all MCP servers used in this project.
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
    
    # Add YOUR NEW MCP server
    try:
        servers.update(get_your_new_mcp_config())
    except ValueError as e:
        print(f"Warning: Could not configure Your New MCP server: {e}")
    
    return servers
```

### Step 3: Add Credentials to `.env`

Add the required credentials to your `.env` file:

```bash
# Your New MCP Server
SERVER_API_KEY=your_api_key_here
SERVER_URL=https://api.example.com
```

## Real Example: Adding JIRA MCP

### 1. Create Function in `config/mcp_config.py`

```python
def get_jira_mcp_config() -> Dict[str, Dict[str, Any]]:
    """
    Get JIRA MCP server configuration.
    
    The JIRA MCP Server provides tools for:
    - Issue management (create, update, search issues)
    - Project tracking (boards, sprints, backlogs)
    - Workflow automation (transitions, assignments)
    
    Returns:
        Dictionary with JIRA MCP server configuration
        
    Raises:
        ValueError: If JIRA credentials are not set
    """
    jira_url = os.getenv("JIRA_URL")
    jira_email = os.getenv("JIRA_EMAIL")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    
    if not jira_url or not jira_email or not jira_api_token:
        raise ValueError(
            "JIRA credentials not set. Required: JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN"
        )
    
    return {
        "jira": {
            "type": "stdio",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-jira"],
            "env": {
                "JIRA_URL": jira_url,
                "JIRA_EMAIL": jira_email,
                "JIRA_API_TOKEN": jira_api_token,
            }
        }
    }
```

### 2. Enable in `get_all_mcp_servers()`

```python
def get_all_mcp_servers() -> Dict[str, Dict[str, Any]]:
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
    
    # Add JIRA MCP server
    try:
        servers.update(get_jira_mcp_config())
    except ValueError as e:
        print(f"Warning: Could not configure JIRA MCP server: {e}")
    
    return servers
```

### 3. Add to `.env`

```bash
# JIRA MCP Server
JIRA_URL=https://your-company.atlassian.net
JIRA_EMAIL=your-email@company.com
JIRA_API_TOKEN=your_jira_api_token_here
```

## That's It! 🎉

Your `autonomous_agent.py` will **automatically** pick up the new MCP server!

No changes needed to:
- ❌ `src/autonomous_agent.py`
- ❌ `examples/*.py`
- ❌ Any other code

## Why This Works

The `AutonomousAgent` class calls `get_all_mcp_servers()` which returns ALL configured servers:

```python
# In autonomous_agent.py (line 68)
mcp_servers = get_all_mcp_servers()  # Gets Datadog + GitHub + JIRA + ...

# Claude Agent SDK automatically loads ALL tools from ALL servers
self.options = ClaudeAgentOptions(
    model=model,
    mcp_servers=mcp_servers,  # All servers passed here
    permission_mode="bypassPermissions"
)
```

## Available MCP Servers

Here are some popular MCP servers you can add:

### Official MCP Servers
- **JIRA** - `@modelcontextprotocol/server-jira`
- **Slack** - `@modelcontextprotocol/server-slack`
- **Google Drive** - `@modelcontextprotocol/server-gdrive`
- **PostgreSQL** - `@modelcontextprotocol/server-postgres`
- **Filesystem** - `@modelcontextprotocol/server-filesystem`

### Community MCP Servers
- **Linear** - Issue tracking
- **Notion** - Documentation
- **Confluence** - Wiki/docs
- **Sentry** - Error tracking
- **PagerDuty** - Incident management

See the [MCP Registry](https://github.com/modelcontextprotocol/servers) for more!

## Testing Your New MCP Server

After adding a new server, test it:

```bash
# Verify it's loaded
./run.sh examples/verify_mcp_servers.py

# Test with a simple query
./run.sh examples/simple_sdk_query.py
```

Then ask Claude to use the new tools:
```python
"List my JIRA issues"
"Create a Slack message"
"Search Google Drive for documents"
```

## Summary

✅ **One file to rule them all**: `config/mcp_config.py`
✅ **Three simple steps**: Create function → Enable → Add credentials
✅ **Zero code changes**: `autonomous_agent.py` stays the same
✅ **Automatic integration**: Claude gets all tools immediately

This design makes it **incredibly easy** to expand your agent's capabilities! 🚀

