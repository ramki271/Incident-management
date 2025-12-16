# Datadog Incident Management Workflow

**Autonomous incident detection, analysis, and fixing** using Claude Agent SDK with Datadog + GitHub MCP servers.

## 🎯 The Vision: Automated Incident Fixing

**Detect → Analyze → Fix → Deploy**

1. 🔍 **Datadog detects** an alert (high error rate, slow queries, etc.)
2. 🧠 **Claude analyzes** logs and metrics to understand the issue
3. 📂 **GitHub access** - Claude reads your repository code
4. 🔬 **Root cause analysis** - Claude identifies the problematic code
5. ✏️ **Creates a fix** - Claude modifies the code
6. 🚀 **Opens a PR** - Claude submits the fix for review

**This is now 100% possible with the integrated MCP servers!**

## ✅ Status: Multi-MCP System with Full Code Access!

### 🔧 Connected MCP Servers
- ✅ **Datadog MCP** - Monitor infrastructure, logs, metrics, incidents (57 monitors, 25 dashboards)
- ✅ **GitHub MCP** - **Full repository access**: Read code, search files, create fixes, open PRs (100+ tools)

### 🎯 Key Capabilities
- ✅ **Detect incidents** in Datadog monitoring
- ✅ **Access repository code** to understand the system
- ✅ **Analyze root causes** by correlating alerts with code
- ✅ **Create fixes** by modifying code files
- ✅ **Open pull requests** with automated fixes
- ✅ **Multi-step autonomous workflows** across both systems
- ✅ **Natural language control** - Just describe what you want

### Examples:

**Simple one-off query:**
```python
import anyio
from src.autonomous_agent import simple_query

async def main():
    result = await simple_query("What monitors are alerting?")
    print(result)

anyio.run(main)
```

**Full agent with context manager:**
```python
import anyio
from src.autonomous_agent import AutonomousAgent

async def main():
    async with AutonomousAgent() as agent:
        # Claude autonomously decides which tools to call!
        result = await agent.query("What monitors are alerting and what's wrong?")

        # Future: Add JIRA MCP and ask:
        # "Create JIRA tickets for each critical alert"
        # Claude will autonomously use both Datadog and JIRA tools!

anyio.run(main)
```

**Quick Start:**
- [examples/simple_sdk_query.py](examples/simple_sdk_query.py) - Simplest usage
- [examples/autonomous_workflow.py](examples/autonomous_workflow.py) - Interactive demo
- [examples/incident_fix_workflow.py](examples/incident_fix_workflow.py) - **Full incident fix automation!**

**Incident Fix Workflow:**
```bash
./run.sh examples/incident_fix_workflow.py
```

This demonstrates the complete vision:
1. Detects Datadog alerts
2. Analyzes the issue
3. Accesses GitHub repository
4. Reads and understands the code
5. Identifies root cause
6. Proposes a fix
7. Can create a PR with the fix

See [docs/INCIDENT_FIX_VISION.md](docs/INCIDENT_FIX_VISION.md) for details!
- [AUTONOMOUS_AGENT_GUIDE.md](AUTONOMOUS_AGENT_GUIDE.md) - How the autonomous agent works
- [SUCCESS_SUMMARY.md](SUCCESS_SUMMARY.md) - Implementation details

## Installation

### Prerequisites

- **Python 3.10+** (required for Claude Agent SDK)
- **Node.js** (for Datadog MCP server)
- **Anthropic API Key** - Get from https://console.anthropic.com/

### Step 1: Install Python Dependencies

**Note:** The Claude Agent SDK requires Python 3.10 or higher. Check your version:
```bash
python3 --version  # Should be 3.10+
```

If you have Python 3.11 installed (recommended):
```bash
# Install dependencies with Python 3.11
pip3.11 install -r requirements.txt

# Or install directly
pip3.11 install claude-agent-sdk anyio python-dotenv
```

### Step 2: Install Datadog MCP Server

The Datadog MCP server is a Node.js package:
```bash
npm install -g datadog-mcp-server
```

We're using [GeLi2001/datadog-mcp-server](https://github.com/GeLi2001/datadog-mcp-server) - a production-ready MCP server with 13.9K downloads.

### Step 3: Configure Environment Variables

Create a `.env` file in the project root with your API credentials:

```bash
# Anthropic API Key (required)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Datadog API Credentials (required)
DD_API_KEY=your_datadog_api_key_here
DD_APP_KEY=your_datadog_application_key_here
DD_SITE=datadoghq.com  # US1 region (app.datadoghq.com)
```

**How to get your API keys:**

**Anthropic API Key:**
1. Go to https://console.anthropic.com/
2. Sign in or create an account
3. Navigate to API Keys
4. Create a new API key

**Datadog API Keys:**
1. Log in to your Datadog account at https://app.datadoghq.com
2. Go to **Organization Settings** → **API Keys**
3. Copy your **API Key**
4. Go to **Organization Settings** → **Application Keys**
5. Create or copy an **Application Key**

### Step 4: Run Examples

The configuration is automatically loaded from `.env` by the application:

```bash
# Simple one-off query
python3.11 examples/simple_sdk_query.py

# Full autonomous workflow demo
python3.11 examples/autonomous_workflow.py

# Run the main agent
python3.11 src/autonomous_agent.py
```

### Available Capabilities

The Datadog MCP server provides these tools:

#### Logs
- **search_logs**: Search Datadog logs with filtering and sorting
  - Query syntax support
  - Time range filtering
  - Service/host filtering
  - Status filtering (error, warn, info, etc.)

#### Metrics
- **query_metrics**: Query available metrics and their metadata
- **get_metric_data**: Retrieve metric values over time

#### Monitoring
- **list_monitors**: Access monitor data and configurations
- **get_monitor**: Get specific monitor details

#### Dashboards
- **list_dashboards**: Retrieve dashboard definitions
- **get_dashboard**: Get specific dashboard data

#### Events & Incidents
- **search_events**: Search events within timeframes
- **list_incidents**: Access incident management data

### Testing

Once configured, you can test the MCP server:

```bash
# Test with MCP Inspector
npx @modelcontextprotocol/inspector datadog-mcp-server

# Or test through Claude Code
# Ask Claude: "Show me recent error logs from Datadog"
```

### Next Steps

After Datadog integration is working:
1. Explore available services in your Datadog account
2. Identify common error patterns
3. Set up JIRA integration for ticket creation
4. Configure code repository access for automated fixes

## Project Status

- ✅ Phase 1: Datadog MCP Server - **COMPLETE**
  - ✅ MCP server installed and configured
  - ✅ Python Agent SDK integration
  - ✅ Configuration module with automatic credential loading
  - ✅ Example usage scripts
  - ✅ Complete documentation
- ⏳ Phase 2: JIRA Integration - Planned
- ⏳ Phase 3: Code Repository Integration - Planned
- ⏳ Phase 4: Autonomous Workflow - Planned

## Project Structure

```
datadog-incident-manager/
├── config/
│   ├── __init__.py
│   └── mcp_config.py          # MCP server configuration
├── src/
│   ├── __init__.py
│   └── datadog_agent.py        # Main agent implementation
├── examples/
│   └── basic_usage.py          # Usage examples
├── .env                        # Your credentials (configured)
├── .env.example                # Template for credentials
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Project metadata
├── setup.sh                    # Automated setup script
├── README.md                   # This file
├── SETUP_GUIDE.md             # Detailed setup instructions
└── ARCHITECTURE.md            # System architecture documentation
```

## Quick Start

### 1. Installation

```bash
# Run automated setup
./setup.sh

# Or manually:
pip install -r requirements.txt
```

### 2. Configuration

Your Datadog credentials are already configured in `.env`. You just need to set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY='your_anthropic_api_key_here'
```

### 3. Test the Setup

```bash
# Test MCP configuration
python config/mcp_config.py

# Run example agent
python src/datadog_agent.py

# Try interactive examples
python examples/basic_usage.py
```

## Usage

### Basic Example

```python
from src.datadog_agent import DatadogAgent

# Initialize the agent
agent = DatadogAgent()

# Search for error logs
errors = agent.search_error_logs(time_range="1h", limit=100)
print(errors)

# Check monitor status
monitors = agent.check_monitor_status()
print(monitors)

# Analyze incidents
incidents = agent.analyze_incident()
print(incidents)
```

### Custom Query

```python
agent = DatadogAgent()

result = agent.query("""
    Analyze the health of our infrastructure in the last 24 hours.
    Look for:
    1. Critical errors
    2. Active incidents
    3. Monitors in alert state
    Provide actionable recommendations.
""")
print(result)
```

## Documentation

- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick reference with code snippets and commands
- **[MCP_EXPLAINED.md](MCP_EXPLAINED.md)** - Understanding MCP servers: Local vs Remote, portability
- **[DEMO_HOW_IT_WORKS.md](DEMO_HOW_IT_WORKS.md)** - Live demonstration of how MCP works behind the scenes
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup instructions for all environments
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture and design details
- **[config/mcp_config.py](config/mcp_config.py)** - MCP configuration (well documented)
- **[src/datadog_agent.py](src/datadog_agent.py)** - Agent implementation (well documented)

## Resources

- [Datadog MCP Server GitHub](https://github.com/GeLi2001/datadog-mcp-server)
- [Datadog API Documentation](https://docs.datadoghq.com/api/latest/)
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [Claude Agent SDK Documentation](https://github.com/anthropics/anthropic-sdk-python)
