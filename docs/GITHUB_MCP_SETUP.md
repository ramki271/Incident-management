# GitHub MCP Server Setup

## Overview

The GitHub MCP Server is GitHub's official Model Context Protocol server that provides AI agents with direct access to GitHub's platform capabilities.

## What Can You Do?

### 🔍 Repository Management
- Browse and query code
- Search files across repositories
- Analyze commits and project structure
- Navigate repository trees

### 🎯 Issue & PR Automation
- Create, update, and manage issues
- Create and manage pull requests
- Review code changes
- Triage bugs automatically
- Manage project boards

### ⚙️ CI/CD & Workflow Intelligence
- Monitor GitHub Actions workflow runs
- Analyze build failures
- Manage releases
- Get insights into development pipeline

### 🔒 Code Analysis
- Examine security findings
- Review Dependabot alerts
- Understand code patterns
- Get comprehensive codebase insights

### 👥 Team Collaboration
- Access discussions
- Manage notifications
- Analyze team activity
- Streamline team processes

## Installation

### Step 1: Install Go

The GitHub MCP Server is written in Go, so you need Go installed:

```bash
# On macOS with Homebrew
brew install go

# Verify installation
go version
```

### Step 2: Install GitHub MCP Server

```bash
# Install the latest version
go install github.com/github/github-mcp-server/cmd/github-mcp-server@latest

# Verify installation
~/go/bin/github-mcp-server --version
```

The binary will be installed at `~/go/bin/github-mcp-server`.

### Step 3: Create GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a descriptive name (e.g., "MCP Server")
4. Select the following scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `read:org` (Read org and team membership)
   - ✅ `read:user` (Read user profile data)
   - ✅ `workflow` (Update GitHub Action workflows)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)

### Step 4: Configure Environment Variables

Add your GitHub token to `.env`:

```bash
# GitHub Personal Access Token for GitHub MCP Server
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here
```

**⚠️ IMPORTANT**: Never commit your `.env` file to git!

### Step 5: Test the Installation

```bash
python examples/test_github_mcp.py
```

This will verify:
- ✓ GitHub MCP Server is installed
- ✓ Configuration is correct
- ✓ Token is valid
- ✓ Connection to GitHub works

## Usage Examples

### Example 1: Simple Query

```python
from claude_agent_sdk import query
from config.mcp_config import get_all_mcp_servers

async for message in query(
    prompt="List my GitHub repositories",
    mcp_servers=get_all_mcp_servers()
):
    print(message)
```

### Example 2: Create an Issue

```python
async for message in query(
    prompt="Create a GitHub issue in my repo 'my-project' titled 'Bug: Login fails' with description 'Users cannot log in'",
    mcp_servers=get_all_mcp_servers()
):
    print(message)
```

### Example 3: Analyze Pull Requests

```python
async for message in query(
    prompt="Show me all open pull requests in my repository and summarize what they do",
    mcp_servers=get_all_mcp_servers()
):
    print(message)
```

### Example 4: Combined Datadog + GitHub Workflow

```python
async for message in query(
    prompt="""
    1. Check Datadog for critical alerts
    2. For each critical alert, create a GitHub issue in my 'ops-tracking' repo
    3. Assign the issues to me
    """,
    mcp_servers=get_all_mcp_servers()
):
    print(message)
```

## Available Tools

The GitHub MCP Server provides 100+ tools organized into categories:

- **Actions**: Workflow runs, artifacts, jobs
- **Code Scanning**: Security alerts, analysis
- **Dependabot**: Dependency alerts, updates
- **Discussions**: Community discussions
- **Events**: Repository events
- **Gists**: Code snippets
- **Git**: Branches, commits, tags, trees
- **Issues**: Issue management, comments, labels
- **Labels**: Label management
- **Notifications**: Notification management
- **Organizations**: Org search and management
- **Projects**: Project boards, items, fields
- **Pull Requests**: PR management, reviews, merges
- **Repositories**: Repo management, files, releases
- **Secret Scanning**: Secret alerts
- **Security Advisories**: Security information
- **Stargazers**: Star management
- **Users**: User search and information

See the full list in the [GitHub MCP Server documentation](https://github.com/github/github-mcp-server).

## Troubleshooting

### "GITHUB_PERSONAL_ACCESS_TOKEN not set"

Make sure you've added your token to `.env`:
```bash
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_actual_token_here
```

### "GitHub MCP Server not found"

Install it with:
```bash
go install github.com/github/github-mcp-server/cmd/github-mcp-server@latest
```

### "Permission denied" errors

Your token might not have the required scopes. Create a new token with:
- `repo`
- `read:org`
- `read:user`
- `workflow`

## Next Steps

1. ✅ Install and configure GitHub MCP Server
2. ✅ Test with `examples/test_github_mcp.py`
3. 📝 Try the examples above
4. 🚀 Build your own workflows combining Datadog + GitHub
5. 🎯 Add JIRA MCP Server for complete incident management

## Resources

- [GitHub MCP Server Repository](https://github.com/github/github-mcp-server)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)

